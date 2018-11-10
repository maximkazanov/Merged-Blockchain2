import datetime
import hashlib
from random import *

class Block:
    blockNo = 0
    data = None
    next = None
    mergeNext = None
    hash = None
    nonce = 0
    previous_hash = 0
    previous_hash1 = 0
    timestamp = datetime.datetime.now()

    def __init__(self, data):
        self.data = data

    def hash(self):
        h = hashlib.sha256()
        h.update(
        str(self.blockNo).encode('utf-8') +
        str(self.data).encode('utf-8') +
        str(self.nonce).encode('utf-8') +
        str(self.previous_hash).encode('utf-8') +
        str(self.previous_hash1).encode('utf-8') +
        str(self.timestamp).encode('utf-8')
        )
        return h.hexdigest()

    def __str__(self):
        return "Block Hash: " + str(self.hash()) + "\nBlockNo: " + str(self.blockNo) + "\nBlock Data: " + str(self.data) + "\nNonce: " + str(self.nonce) + "\n--------------"

class Blockchain:

    diff = 5
    maxNonce = 2**32
    target = 2 ** (256-diff)
    block = None
    head = None
    head1 = None
    def __init__(self, genesis=None):

        self.block = Block(genesis)
        dummy = self.head = self.block

    def add(self, block):

        block.previous_hash = self.block.hash()
        block.blockNo = self.block.blockNo + 1

        self.block.next = block
        self.block = self.block.next

    def mine(self, block):
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                self.add(block)
                break
            else:
                block.nonce += 1

def merge(blockchain, blockchain1):
    mergedBlockChain = Blockchain()
    mergeBlock = Block(blockchain.block.data + blockchain1.block.data)


    mergedBlockChain.head = blockchain.head
    mergedBlockChain.head1 = blockchain1.head


    for n in range(max(blockchain.maxNonce, blockchain1.maxNonce)):
        if int(mergeBlock.hash(), 16) <= max(blockchain.target, blockchain1.target):
            mergeBlock.previous_hash = blockchain.block.hash()
            mergeBlock.previous_hash1 = blockchain1.block.hash()
            mergeBlock.blockNo = max(blockchain.block.blockNo, blockchain1.block.blockNo) + 1
            mergedBlockChain.block.next = mergeBlock
            mergedBlockChain.block = mergedBlockChain.block.next
            break
        else:
                mergeBlock.nonce += 1

    mergeBlock.blockNo = max(blockchain.block.blockNo, blockchain1.block.blockNo) + 1

    blockchain.block.mergeNext = mergeBlock
    blockchain1.block.mergeNext = mergeBlock   

    return mergedBlockChain

blockchain1 = Blockchain("Genesis 1")
blockchain2 = Blockchain("Genesis 2")

for n in range(10):
    r = random()
    if r > 0.5:
        blockchain1.mine(Block("Block " + str(n+1)))
    else:
        blockchain2.mine(Block("Block " + str(n+1)))

mergedBC1 = merge (blockchain1,blockchain2)

for n in range(10,20):
    r = random()
    if r > 0.5:
        blockchain1.mine(Block("Block " + str(n+1)))
    else:
        blockchain2.mine(Block("Block " + str(n+1)))

for n in range(20,25):
    mergedBC1.mine(Block("Block " + str(n+1)))

print ("Blockchain 1:")
num = 0
while blockchain1.head != None:
    print(blockchain1.head)
    num = num + 1
    blockchain1.head = blockchain1.head.next
print ("Total number of blocks in Blockchain 1: " + str(num))

print ("\nBlockchain 2:")
num = 0
while blockchain2.head != None:
    print(blockchain2.head)
    num = num + 1
    blockchain2.head = blockchain2.head.next
print ("Total number of blocks in Blockchain 2: " + str(num))

print ("\nBlockchain Merged Blockchain 1:")
num = 0
print(mergedBC1.head)
num = num + 1
while not (mergedBC1.head.next == None and mergedBC1.head.mergeNext == None):
    if mergedBC1.head.mergeNext == None:
        print(mergedBC1.head.next)
        num = num + 1
        mergedBC1.head = mergedBC1.head.next
    else:
        print(mergedBC1.head.mergeNext)
        num = num + 1
        mergedBC1.head = mergedBC1.head.mergeNext
while mergedBC1.head1 != None:
    print(mergedBC1.head1)
    num = num + 1
    if mergedBC1.head1.mergeNext != None:
        break
    mergedBC1.head1 = mergedBC1.head1.next
print ("Total number of blocks in Merged Blockchain 1: " + str(num))