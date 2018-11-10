import datetime
import hashlib
from random import *

class Block:
    blockNo = 0
    data = None
    next = None
    mergeNext = None #Added field to store pointer to a "connector" block
    hash = None
    nonce = 0
    previous_hash = 0 
    previous_hash1 = 0 #For a block which is a "connector" block, 2 previous hashes will be stored
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
    head1 = None #Changing definitio so that a blockchain can store 2 heads
    def __init__(self, genesis=None):

        self.block = Block(genesis) #With previous implementation when I created 2 blockchains, both would originate from the same Genesis block
        dummy = self.head = self.block #so this implementation assumes at initialization different Genesis's name can be passed

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

def merge(blockchain, blockchain1): #new method to merge 2 blockchains
    mergedBlockChain = Blockchain() #creating new blockchain with empty Genesis
    mergeBlock = Block(blockchain.block.data + blockchain1.block.data) #Connector block is created with a data equal to concat. data of last blocks in 2 merged blockchains

    #Setting 2 heads of a "merged" blockchain
    mergedBlockChain.head = blockchain.head 
    mergedBlockChain.head1 = blockchain1.head

    #mining connector block and adding it to merged blockchain
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

    mergeBlock.blockNo = max(blockchain.block.blockNo, blockchain1.block.blockNo) + 1 #arbitrary setting connector's block no. = max of no. of last blocks in 2 blockcains to be merged

    blockchain.block.mergeNext = mergeBlock
    blockchain1.block.mergeNext = mergeBlock   

    return mergedBlockChain
#trying it
blockchain1 = Blockchain("Genesis 1")
blockchain2 = Blockchain("Genesis 2")
#randomly assigning 10 blocks to 2 blockcains
for n in range(10):
    r = random()
    if r > 0.5:
        blockchain1.mine(Block("Block " + str(n+1)))
    else:
        blockchain2.mine(Block("Block " + str(n+1)))
#calling merge method to merge 2 newly created and populated blockchains
mergedBC1 = merge (blockchain1,blockchain2)
#again randomly assigning 10 blocks to 2 blockcains
for n in range(10,20):
    r = random()
    if r > 0.5:
        blockchain1.mine(Block("Block " + str(n+1)))
    else:
        blockchain2.mine(Block("Block " + str(n+1)))

#adding 5 blocks to a merged blockchain
for n in range(20,25):
    mergedBC1.mine(Block("Block " + str(n+1)))


#Displaying content of first blockchain. Keeping track of no. of blocks.
print ("Blockchain 1:")
num = 0
while blockchain1.head != None:
    print(blockchain1.head)
    num = num + 1
    blockchain1.head = blockchain1.head.next
print ("Total number of blocks in Blockchain 1: " + str(num))

#Displaying content of second blockchain. Keeping track of no. of blocks. Total number of blocks in 
#2 blockchains shall be 22 = 2 genesis blocks and 20 randomly assigned blocks

print ("\nBlockchain 2:")
num = 0
while blockchain2.head != None:
    print(blockchain2.head)
    num = num + 1
    blockchain2.head = blockchain2.head.next
print ("Total number of blocks in Blockchain 2: " + str(num))

#Displaying merged blockchain and keeping track of number of blocks. Shall be 18 = 10 blocks from 2 chains before merger + 2 genesis blocks + 1 connector block.
print ("\nBlockchain Merged Blockchain 1:")
num = 0
#Displaying 1st genesis
print(mergedBC1.head)
num = num + 1
#Displaying all following blocks of 1st chain before merger + connector block + 5 blocks added to a chain after merger
while not (mergedBC1.head.next == None and mergedBC1.head.mergeNext == None):
    if mergedBC1.head.mergeNext == None:
        print(mergedBC1.head.next)
        num = num + 1
        mergedBC1.head = mergedBC1.head.next
    else:
        print(mergedBC1.head.mergeNext)
        num = num + 1
        mergedBC1.head = mergedBC1.head.mergeNext
#Displaying blocks originating from second genesis block up to "connector" block
while mergedBC1.head1 != None:
    print(mergedBC1.head1)
    num = num + 1
    if mergedBC1.head1.mergeNext != None:
        break
    mergedBC1.head1 = mergedBC1.head1.next
print ("Total number of blocks in Merged Blockchain 1: " + str(num))