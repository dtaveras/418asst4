// Copyright 2013 Harry Q. Bovik (hbovik)

#include <glog/logging.h>
#include <stdio.h>
#include <stdlib.h>

#include "server/messages.h"
#include "server/master.h"

#define DBG_1

static struct Master_state {

  bool server_ready;

  int max_num_workers;
  int num_active_workers;
  int current_worker;

  int total_pending_client_requests;
  int max_req_pos;

  Worker_handle* workers;
  std::map<Worker_handle, int> num_req_map;
  std::vector<Client_handle> waiting_clients;

} mstate;


void master_node_init(int max_workers, int& tick_period) {

  // set up tick handler to fire every 5 seconds. (feel free to
  // configure as you please)
  tick_period = 5;
  mstate.max_num_workers = max_workers;
  mstate.total_pending_client_requests = 0;
  mstate.num_active_workers = 0;
  mstate.max_req_pos = 0;
  mstate.current_worker = 0;

  int max_num_workers = mstate.max_num_workers;
  mstate.workers = (Worker_handle*)malloc(sizeof(Worker_handle)*max_num_workers);

  mstate.server_ready = false;

  // fire off requests for new workers
  int tag;
  for(int i=0; i< max_num_workers; i++){
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

  mstate.workers[tag] = worker_handle;
  mstate.num_req_map[worker_handle] = 0;
  mstate.num_active_workers += 1;

  //After all workers have booted tell the system we are ready to receive requests
  if(mstate.num_active_workers == mstate.max_num_workers && !mstate.server_ready)
    {
      printf("Server Finished Initializing ....\n");
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
    Response_msg resp(0);
    resp.set_response("ack");
    send_client_response(client_handle, resp);
    return;
  }

  int tag = mstate.max_req_pos++;
  
#ifdef DBG_1  
  printf("------------------------------------------------\n");

  printf("[Assign_To_Wrk:%d | Tag: %d | total_pending_requests:%d]\n", 
	 mstate.current_worker, tag, mstate.total_pending_client_requests);

  printf("[");
  for(int i = 0; i< mstate.num_active_workers; i++){
    printf(" wrk%d: %d ", i, mstate.num_req_map[mstate.workers[i]] );
  }
  printf("]\n");

  printf("------------------------------------------------\n");
#endif

  mstate.waiting_clients.push_back(client_handle);
  mstate.total_pending_client_requests += 1;
  mstate.num_req_map[mstate.workers[mstate.current_worker]] += 1;

  Request_msg worker_req(tag, client_req);
  send_request_to_worker(mstate.workers[mstate.current_worker], worker_req);

  //Manage Round Robin state
  if(mstate.current_worker == mstate.max_num_workers-1)
    mstate.current_worker = 0;
  else
    mstate.current_worker += 1;

  // We're done!  This event handler now returns, and the master
  // process calls another one of your handlers when action is required.
}


void handle_tick() {

  // TODO: you may wish to take action here.  This method is called at
  // fixed time intervals, according to how you set 'tick_period' in
  // 'master_node_init'.

}

