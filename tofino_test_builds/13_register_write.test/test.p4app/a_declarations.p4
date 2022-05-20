Register< bit<64>, bit<64> >(10) msgbox_a;
Register< bit<64>, bit<64> >(10) msgbox_b;
RegisterAction<bit<64>,bit<64>,bit<64>>(msgbox_a) read_shared_array_action_uid2 = {
void apply(inout bit<64> stored_value, out bit<64> to_return){
		to_return = stored_value;
	}
};
RegisterAction<bit<64>,bit<64>,bit<64>>(msgbox_b) write_shared_array_action_uid3 = {
void apply(inout bit<64> to_store){
		to_store = tmp;
	}
};
