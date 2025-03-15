# tm/machine.py

import math
from utils import *

class TuringMachine:
    def __init__(self, tape_bits, head_bits, state_bits, binary_input=None, probability=0.5):

        self.tape = None
        self.head_bits = head_bits
        self.state_bits = state_bits
        self.trans_prob = probability
        
        # Initialize tape
        if binary_input is None:
            binary_input = generate_random_input(tape_bits)
        self.binary_input = binary_input
        self.tape = list(binary_input)

        # Initialize machine's internal info
        self.outcome = None
        self.head_position = 1
        self.current_state = 0
        
        self.transition_function = generate_random_transitions(self)

        self.config_history = set()
        self.config_bits = tape_bits + head_bits + state_bits


    def move_head(self, direction):
        # Head and tape might not align, so we need to bound the head
        limit = min(len(self.tape) - 1, 2 ** self.head_bits - 1)
        if direction == 'R' and self.head_position < limit:
            self.head_position += 1
        elif direction == 'L' and self.head_position > 0:
            self.head_position -= 1
        
    def step(self):
        """
        Executes a single transition step. If no transition is found for the current (state, symbol),
        the machine halts.
        """
        current_symbol = self.tape[self.head_position]
        transition = self.transition_function.get((self.current_state, current_symbol))
        
        if not transition:
            return "halt"
        
        next_state, write_symbol, direction = transition
        self.current_state = next_state
        self.tape[self.head_position] = write_symbol
        self.move_head(direction)        

    def run(self):
        """
        Runs the Turing Machine, recording configurations in self.config_history,
        until it halts or enters a loop.
        """
        
        while True:
            result = self.step()
            current_config = get_configuration(self)
            if result is not None: # Machine halted
                self.config_history.add(current_config)
                self.outcome = "halt"  
                break
            if current_config in self.config_history: # Entering a loop
                self.outcome = "loop"
                break
            self.config_history.add(current_config)  
