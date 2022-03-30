#include <pif_plugin.h>
#include <nfp.h>
#include <mem_atomic.h>
#include <nfp_mem_lockq.h>

__declspec(imem export aligned(64)) int global_semaphore_active;
__declspec(imem export aligned(64)) int global_semaphore_sold;

__declspec(imem export aligned(64)) struct mem_lockq256_t global_semaphore;

void atomic_begin() {
    //int my_ticket = global_semaphore_sold++;
    //while (my_ticket!=global_semaphore_active){};
    
    SIGNAL_PAIR pair;
    do {
        cmd_mem_lockq256_lock_ptr40(&global_semaphore,sig_done,&pair);
    } while( signal_test(&pair.odd) );
}

void atomic_end() {
    //++global_semaphore_active;
    cmd_mem_lockq256_unlock_ptr40(&global_semaphore);
}

void pif_plugin_init_master() {
    global_semaphore_active = 1;
	global_semaphore_sold = 0; 
    cmd_mem_lockq256_init_ptr40(&global_semaphore,0,0); 
}

void pif_plugin_init() {
}

int pif_plugin_atomic_begin(EXTRACTED_HEADERS_T *headers, MATCH_DATA_T *data) {
    atomic_begin();
    return PIF_PLUGIN_RETURN_FORWARD;
}

int pif_plugin_atomic_end(EXTRACTED_HEADERS_T *headers, MATCH_DATA_T *data) {
    atomic_end();
    return PIF_PLUGIN_RETURN_FORWARD;
}