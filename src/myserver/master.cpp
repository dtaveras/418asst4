// Copyright 2013 Harry Q. Bovik (hbovik)

#include <glog/logging.h>
#include <stdio.h>
#include <stdlib.h>

#include "server/messages.h"
#include "server/master.h"
#include "tools/work_queue.h"
//#include <boost/unordered_map.hpp>

#define DBG_1
#define MAX_WORKER_JOBS 2

//Text Color Options
#define BLACK 0
#define RED 1
#define GREEN 2
#define YELLOW 3
#define BLUE 4
#define MAGENTA 5
#define CYAN 6
#define WHITE 7

static void textcolor(unsigned int color)
{
  printf("%c[%d;%d;%dm",0x1B,0,30 + color,40);
}

static struct Master_state {

  bool server_ready;
  bool serv_worker_req; //Are we servicing a new worker request

  Request_msg pending_msg;

  int max_num_workers;
  int num_active_workers;
  int starting_num_workers;

  int total_pending_client_requests;
  int work_queue_size;
  int max_req_pos;
  
  Worker_handle* workers;
  std::vector<int> free_workers;
  std::map<Worker_handle, int> num_req_map; //Number of pending requests
  std::vector<Client_handle> waiting_clients;
  
  WorkQueue<Request_msg> work_queue;
} mstate;

void master_node_init(int max_workers, int& tick_period) {

  // set up tick handler to fire every # of seconds
  tick_period = 5;
  mstate.max_num_workers = max_workers;
  mstate.total_pending_client_requests = 0;
  mstate.num_active_workers = 0;
  mstate.max_req_pos = 0;
  mstate.work_queue_size = 0;
  mstate.starting_num_workers = 1;
  mstate.serv_worker_req = false;
  mstate.work_queue = WorkQueue<Request_msg>();

  int max_num_workers = mstate.max_num_workers;
  mstate.workers = (Worker_handle*)malloc(sizeof(Worker_handle)*max_num_workers);
  //initialize
  for(int i = 0; i< mstate.max_num_workers; i++){
    mstate.workers[i] = NULL;
  }

  mstate.server_ready = false;

  // fire off requests for new workers
  int tag;
  for(int i=0; i< mstate.starting_num_workers; i++){
    tag = i;
    Request_msg req(tag);
    req.set_arg("name", "my worker");
    request_new_worker_node(req);
  }
}

void handle_new_worker_online(Worker_handle worker_handle, int tag) {
  // 'tag' allows you to identify which worker request this response
  // corresponds to.  Since the starter code only sends off one new
  // worker request, we don't use it here.
  
  if(mstate.serv_worker_req){
    textcolor(RED);
    printf("[servicing new worker plus client request]\n");
    textcolor(WHITE);
    send_request_to_worker(worker_handle, mstate.pending_msg);

    mstate.num_active_workers += 1;
    mstate.workers[tag] = worker_handle;
    mstate.num_req_map[worker_handle] += 1;

    mstate.serv_worker_req = false;
  }
  else{
    mstate.num_active_workers += 1;
    mstate.workers[tag] = worker_handle;
    mstate.num_req_map[worker_handle] = 0; //clear requests
  }

  //After all workers have booted tell the system we are ready to receive requests
  if(mstate.num_active_workers == mstate.starting_num_workers && !mstate.server_ready)
    {
      textcolor(YELLOW);
      printf("Server Finished Initializing ....\n");
      textcolor(WHITE);

      mstate.server_ready = true;
      server_init_complete();
    }
}

void handle_worker_response(Worker_handle worker_handle, const Response_msg& resp) {
  // Master node has received a response from one of its workers.
  int tag = resp.get_tag();
  send_client_response(mstate.waiting_clients[tag], resp);

  mstate.num_req_map[worker_handle] -= 1;
  mstate.total_pending_client_requests -= 1;
}

void handle_client_request(Client_handle client_handle, const Request_msg& client_req) {
  // You can assume that traces end with this special message.  It
  // exists because it might be useful for debugging to dump
  // information about the entire run here: statistics, etc.
  if (client_req.get_arg("cmd") == "lastrequest") {
    while(mstate.total_pending_client_requests == 0){};
    Response_msg resp(0);
    resp.set_response("ack");
    send_client_response(client_handle, resp);
    return;
  }

  int tag = mstate.max_req_pos++;
  Request_msg worker_req(tag, client_req);

  mstate.waiting_clients.push_back(client_handle);
  mstate.total_pending_client_requests += 1;

  //Check if there are any active workers with less than max number of jobs
  for(int i=0; i< mstate.max_num_workers; i++){
    if( mstate.workers[i] != NULL &&
	mstate.num_req_map[mstate.workers[i]] < MAX_WORKER_JOBS ){
      textcolor(GREEN);
      printf("[Send Request to active worker: %d]\n",i);
      textcolor(WHITE);
      mstate.num_req_map[mstate.workers[i]] += 1;
      send_request_to_worker(mstate.workers[i], worker_req);
      return;
    }
  }
  
  // Already asking for new worker lets just put this request in the work queue
  if(mstate.serv_worker_req){
    textcolor(MAGENTA);
    printf("[Add Request to the Work_Queue]\n");
    textcolor(WHITE);
    //add to work_queue
    mstate.work_queue.put_work(worker_req);
    mstate.work_queue_size += 1;
    return;
  }

  // Lets ask for a new worker or add the request to the work queue
  Request_msg req_for_worker;
  int wkr_tag;
  if(mstate.free_workers.size() != 0){
    wkr_tag = mstate.free_workers.back(); // Get last
    mstate.free_workers.pop_back(); // remove last

    req_for_worker.set_tag(wkr_tag);
    req_for_worker.set_arg("name", "another worker");
    // set the global state
    mstate.serv_worker_req = true;
    mstate.pending_msg = worker_req;
    request_new_worker_node(req_for_worker);
    return;
  }
  else if(mstate.num_active_workers < mstate.max_num_workers){
    wkr_tag = mstate.num_active_workers;
    req_for_worker.set_tag(wkr_tag);
    req_for_worker.set_arg("name", "another worker");
    // set the global state
    mstate.serv_worker_req = true;
    mstate.pending_msg = worker_req;
    request_new_worker_node(req_for_worker);
    return;
  }
  else{// system is filled add request to the work_queue
    textcolor(MAGENTA);
    printf("[Add Request to the Work_Queue]\n");
    textcolor(WHITE);
    //add to work queue
    mstate.work_queue.put_work(worker_req);
    mstate.work_queue_size += 1;
    return;
  }
  
  // We're done!  This event handler now returns, and the master
  // process calls another one of your handlers when action is required.
}

void handle_tick() {
  // TODO: you may wish to take action here.  This method is called at
  // fixed time intervals, according to how you set 'tick_period' in
  // 'master_node_init'.
  printf("handling tick\n");
  printf("[Worker_Queue_Size: %d]\n", mstate.work_queue_size);
  if(mstate.work_queue_size > 0){
    Request_msg req = mstate.work_queue.get_work();
    for(int i=0; i< mstate.max_num_workers; i++){
      if( mstate.workers[i] != NULL &&
	  mstate.num_req_map[mstate.workers[i]] < MAX_WORKER_JOBS ){
	mstate.num_req_map[mstate.workers[i]] += 1;
	send_request_to_worker(mstate.workers[i], req);
	mstate.work_queue_size -= 1;
	return;
      }
    }
  }

}
