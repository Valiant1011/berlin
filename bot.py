from utils import *
import random, copy

class Object:
    """This represents any physical object that can appear in an Environment.
    You subclass Object to get the objects you want.  Each object can have a
    .__name__  slot (used for output only)."""

    def __repr__(self):
        return '<%s>' % getattr(self, '__name__', self.__class__.__name__)

    def is_alive(self):
        """Objects that are 'alive' should return true."""
        return hasattr(self, 'alive') and self.alive

    def display(self, canvas, x, y, width, height):
        """Display an image of this Object on the canvas."""
        print(__name__, 'exists')
        pass

class Agent(Object):
    """An Agent is a subclass of Object with one required slot,
    .program, which should hold a function that takes one argument, the
    percept, and returns an action. (What counts as a percept or action
    will depend on the specific environment in which the agent exists.)
    Note that 'program' is a slot, not a method.  If it were a method,
    then the program could 'cheat' and look at aspects of the agent.
    It's not supposed to do that: the program can only look at the
    percepts.  An agent program that needs a model of the world (and of
    the agent itself) will have to build and maintain its own model.
    There is an optional slots, .performance, which is a number giving
    the performance measure of the agent in its environment."""
    is_alive = True
    def TraceAgent(agent):
        """Wrap the agent's program to print its input and output. This will let
        you see what the agent is doing in the environment."""
        def new_program(percept):
            action = agent.program(percept)
            print('%s perceives %s and does %s' % (agent, percept, action))
            return action
        agent.program = new_program
        return agent

class TableDrivenAgent(Agent):
    """This agent selects an action based on the percept sequence.
    It is practical only for tiny domains.
    To customize it you provide a table to the constructor. [Fig. 2.7]"""
    def __init__(self):
        # The agent program could in principle be a function, but because
        # it needs to store state, we make it a callable instance of a class.
        Agent.__init__(self)
        percepts = []
        self.table = self.TableDrivenChatResponses()

    def program(self, percept):
        try:
            keys = self.table.keys()
            for key in keys:
                for entry in key:
                    if entry == percept:
                        action = self.table.get(key)
                        return action
        except:
            # print('Could not find action for ', percept)
            action = 'Hmm...'

        return action
        
    def TableDrivenChatResponses(self):
        table = {
                    ('hi', 'hello', 'hey there', 'hey', ): 'Hello! How are you?',
                    ('i am fine', ): 'That is great! How may I help you?',
                    ('i am not fine', ): 'That is sad! How may I help you?',
                    ('can you help me', ): 'Of course! What\'s your problem?',
                    ('i need information about my order', ): 'What is your order ID?',
                    ('12345', ): 'Fetching data from our servers...',
                    ('forgot it', 'i dont know', ): 'Can you check on your reciept for the order ID?',
                    ('yes', ): 'Okay!',
                    ('no', ): 'sorry?',
                    ('service agent', 'human', 'call service agent', ): 'Calling our human friend... Please wait for some time!',
                    ('what is your name', 'what is your name?', ): 'My name is Berlin!',
                    ('nice name', 'nice name!', ): 'Thank you!',
                    ('i remember my order id', ): 'Nice! What is it?',
                    ('elaborate', ): 'Wait a moment, fetching data from our servers...',
                    ('', ' ' ): 'Hmm...',
                    ('bye', 'see ya', 'exit', 'quit', ): 'Bye',
                    ('tell me about my order', ): 'It\'s under process. It should reach you in about 2 days.',
            }

        return table

class Environment:
    """Abstract class representing an Environment.  'Real' Environment classes
    inherit from this. Your Environment will typically need to implement:
        percept:           Define the percept that an agent sees.
        execute_action:    Define the effects of executing an action.
                           Also update the agent.performance slot.
    The environment keeps a list of .objects and .agents (which is a subset
    of .objects). Each agent has a .performance slot, initialized to 0.
    Each object has a .location slot, even though some environments may not
    need this."""

    def __init__(self):
        self.objects = []
        self.agents = []
        object_classes = [] ## List of classes that can go into environment

    # def percept(self, agent):
    #     #Return the percept that the agent sees at this point. Override this.
    #     query = input('Enter Query >')  
    #     return self.execute_action(agent,query)
    
    # def execute_action(self, agent, query):
    #     #"Change the world to reflect this action. Override this."
    #     return agent.program(query)

    # def exogenous_change(self):
    #     pass
    #     #"If there is spontaneous change in the world, override this."

    # def is_done(self):
    #     for agent in self.agents:
    #         if agent.is_alive(): 
    #             return False
    #     return True

    # def step(self):
    #     if not self.is_done():
    #         actions = [agent.program(self.percept(agent))
    #                    for agent in self.agents]
    #         for (agent, action) in zip(self.agents, actions):
    #             self.execute_action(agent, action)
    #         self.exogenous_change()
            

    def run(self, steps = 1000):
    #"""Run the Environment for given number of time steps."""
        # for step in range(steps):
        #     if self.is_done(): 
        #         return
        #     self.step()
        agent = self.agents[0]
        for i in range (0, steps):
            query = input('Enter query > ')
            response = agent.program(query)
            print('Response > ', response)
            if response == 'Bye':
                break

    def add_object(self, object):
    #"""Add an object to the environment, setting its location. Also keep
    #track of objects that are agents.  Shouldn't need to override this."""
        self.objects.append(object)
        if isinstance(object, Agent):
            self.agents.append(object)

