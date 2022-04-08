Register< bit<32>, bit<32> >(10) counter_register;
RegisterAction<bit<32>,bit<32>,bit<32>>(counter_register) increment_register_action_uid2 = {
void apply(inout bit<32> to_store, out bit<32> to_return){
		to_store = to_store + 1;
		to_return = to_store;
	}
};
