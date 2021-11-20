// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.25 <7.0.0;

contract MyContract{
    uint public totSuccess = 0; // count of successful transactions
    /*
    struct Queue {
        uint[] items;
        uint size;
        uint head;
    }
    
    function create(Queue storage self, uint size) internal {
        self.size = size;
        self.head = 0;
        delete self.items;
    }
    function append(Queue storage self, uint item) internal
    returns (bool result) {
        self.items.push(item);
        self.size++;
        return true;
    }
    function remove(Queue storage self) internal 
    returns (uint item) {
        item = self.items[self.head];
        self.head++;
    }*/

    struct User{ // struct to define a user
        uint user_id;
    	string user_name;
        mapping(uint=>uint) edge_list; // connected users mapped to the corresponding balance
    }
    
    mapping(uint=>User) allUsers;
    
    function registerUser(uint user_id, string user_name) public{
        	allUsers[user_id] = User(user_id, user_name);
    }
    
    function createAcc(uint user_id_1, uint user_id_2, uint amt) public{
            allUsers[user_id_1].edge_list[user_id_2] = amt;
            allUsers[user_id_2].edge_list[user_id_1] = amt;
    }
    
    function check(uint user_id_1, uint user_id_2) public view returns (uint){
        return allUsers[user_id_1].edge_list[user_id_2];
    }
    
    
    bool flag;
    mapping(uint=>uint) parent;
    mapping(uint=>bool) visited;
    
    function findPath(uint source, uint amt) public{ // bfs to find the shortest path
        visited[source] = true;
        for(uint i=0;i<100;i++){
            if(allUsers[source].edge_list[i]>amt && !visited[i]){
                parent[i] = source;
                findPath(i,amt);
            }
        }
    }
    
    function sendAmount(uint user_id_1, uint user_id_2, uint amt) public{
        /*Queue storage q;
        create(q,0);
        append(q,user_id_1);*/
        // find shortest path with valid balances and execute transaction
        
        for(uint j=0;j<100;j++) visited[j] = false;
        parent[user_id_2] = user_id_2;
        findPath(user_id_1,amt);
        // iterate through parents to get to source user from destination user
        if(parent[user_id_2]!=user_id_2){
            uint temp = user_id_2;
            while(temp!=user_id_1){
                allUsers[parent[temp]].edge_list[temp] -= amt;
                allUsers[temp].edge_list[parent[temp]] += amt;
                temp = parent[temp];
            }
            flag = true;
            totSuccess++;
        }
        else{flag=false;}
    }
    // function for debugging
    function checkFlag() public view returns (bool){
        return flag;
    }
    
    function getSucCount() public view returns (uint){
        return totSuccess;
    }
    // closes link - makes balance zero, so never usable
    function closeAcc(uint user_id_1, uint user_id_2) public{
        allUsers[user_id_1].edge_list[user_id_2] = 0;
        allUsers[user_id_2].edge_list[user_id_1] = 0;
    }
    
}
