import datetime as _dt
import hashlib as _hashlib
import json as _json

class Blockchain:

    def __init__(self) -> None:
        self.chain = list()
        genesis_block = self._proof_of_work(
            previous_hash="0",
            index= 0,
            data="this is the genesis block")
        self.chain.append(genesis_block)

    def mine_block(self,data:str) -> dict:
        previous_block = self.get_previous_block()
        index = previous_block["index"]+1
        previous_hash = self._hash(block=previous_block)
        block = self._proof_of_work(previous_hash,index,data)
        self.chain.append(block)
        return block
        
    def _proof_of_work(self,previous_hash:str,index:int,data:str) -> int:
        new_proof = 0
        check_proof = False

        block = self._create_block(
            previous_hash=previous_hash,
            index=index,
            data=data,
            proof=new_proof
        )

        while not check_proof:
            
            hash_val = self._hash(block)

            if hash_val[:4]=="0000":
                check_proof=True
            else:
                block["proof"]+=1

        return block

    def _hash(self,block:dict) ->  str:
         encoded_block = _json.dumps(block,sort_keys=True).encode()
         return _hashlib.sha256(encoded_block).hexdigest()

    def get_previous_block(self) -> dict:
        return self.chain[-1]

    def _create_block(self,index:int,data:str,previous_hash:str,proof:int) -> dict:
        block = {
            "previous_hash":previous_hash,
            "index":index,
            "timestamp":str(_dt.datetime.now()),
            "data":data,
            "proof":proof,
        }

        return block
    
    def is_chain_valid(self) -> bool:

        current_block = self.chain[0]
        block_index = 0

        while block_index < len(self.chain)-1:
            next_block = self.chain[block_index+1]
            hash_val_curr_block = self._hash(current_block)

            if (next_block["previous_hash"]!=hash_val_curr_block) or (hash_val_curr_block[:4]!="0000"):
                return False
            
            current_block = next_block
            block_index+=1

        return True
