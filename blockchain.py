import datetime as _dt
import hashlib as _hashlib
import json as _json

class Blockchain:

    def __init__(self) -> None:
        self.chain = list()
        genesis_block = self._create_block(
            index=0,
            data="this is the genesis block",
            previous_hash="0",
            proof=0,)
        self.chain.append(genesis_block)

    def mine_block(self,data:str) -> dict:
        previous_block = self.get_previous_block()
        previous_proof = previous_block["proof"]
        index = previous_block["index"]+1
        proof = self._proof_of_work(previous_proof,index,data)
        previous_hash = self._hash(block=previous_block)
        block = self._create_block(
            data=data,
            index=index,
            previous_hash=previous_hash,
            proof=proof
        )
        self.chain.append(block)
        return block

    def _hash(self,block:dict) ->  str:
         encoded_block = _json.dumps(block,sort_keys=True).encode()
         return _hashlib.sha256(encoded_block).hexdigest()

    def _to_digest(self,new_proof:int,previous_proof:int,index:str,data:str) -> bytes:
        to_digest = str(new_proof**2 - previous_proof**20)*index + data
        return to_digest.encode()
        
    def _proof_of_work(self,previous_proof:int,index:int,data:str) -> int:
        new_proof = 0
        check_proof = False

        while not check_proof:
            to_digest = self._to_digest(
                new_proof=new_proof,
                previous_proof=previous_proof,
                index=index,
                data=data,)
            hash_val = _hashlib.sha256(to_digest).hexdigest()

            if hash_val[:4]=="0000":
                check_proof=True
            else:
                new_proof+=1

        return new_proof


    def get_previous_block(self) -> dict:
        return self.chain[-1]

    def _create_block(self,index:int,data:str,previous_hash:str,proof:int) -> dict:
        block = {
            "index":index,
            "timestamp":str(_dt.datetime.now()),
            "data":data,
            "proof":proof,
            "previous_hash":previous_hash,
        }

        return block
    
    def is_chain_valid(self) -> bool:

        current_block = self.chain[0]
        block_index = 0

        while block_index < len(self.chain)-1:
            next_block = self.chain(block_index+1)

            if next_block["previous_hash"]!=self._hash(current_block):
                return False
            
            hash_val = _hashlib.sha256(
                self._to_digest(
                new_proof=next_block["proof"],
                previous_proof=current_block["proof"],
                index=next_block["index"],
                data=next_block["data"]
                )
            ).hexdigest()

            if hash_val[:4]!="0000":
                return False
            
            current_block = next_block
            block_index+=1

        return True
