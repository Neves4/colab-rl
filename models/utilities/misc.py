""""""

#!/usr/bin/env python

import numpy as np
from argparse import ArgumentParser

import tensorflow as tf

try:
    from keras import backend as K
except ImportError:
    from tensorflow.keras import backend as K

__author__ = "Victor Neves"
__license__ = "MIT"
__maintainer__ = "Victor Neves"
__email__ = "victorneves478@gmail.com"


class LinearSchedule(object):
    def __init__(self, schedule_timesteps, final_p, initial_p):
        """Linear interpolation between initial_p and final_p over
        schedule_timesteps. After this many timesteps pass final_p is
        returned.
        Parameters
        ----------
        schedule_timesteps: int
            Number of timesteps for which to linearly anneal initial_p
            to final_p
        initial_p: float
            initial output value
        final_p: float
            final output value
        """
        self.schedule_timesteps = schedule_timesteps
        self.final_p = final_p
        self.initial_p = initial_p

    def value(self, t):
        """See Schedule.value"""
        fraction = min(float(t) / self.schedule_timesteps, 1.0)
        return self.initial_p + fraction * (self.final_p - self.initial_p)


class HandleArguments:
        """Handle arguments provided in the command line when executing the model.

        Attributes:
            args: arguments parsed in the command line.
            status_load: a flag for usage of --load argument.
            status_visual: a flag for usage of --visual argument.

            NEED UPDATE!
        """
        def __init__(self):
            self.parser = ArgumentParser()
            self.parser.add_argument("-load", help = "load a previously trained model. the argument is the filename", required = False, default = "", type = str)
            self.parser.add_argument("-cnn_model", help = "choose the cnn model used", required = False, default = "CNN3", type = str)
            self.parser.add_argument("-error", help = "choose the loss function for the cnn model", required = False, default = "huber_loss", type = str)
            self.parser.add_argument("--visual", help = "define board size", required = False, action = 'store_true')
            self.parser.add_argument("--dueling", help = "use dueling DQN", required = False, action = 'store_true')
            self.parser.add_argument("--double", help = "use double DQN", required = False, action = 'store_true')
            self.parser.add_argument("--per", help = "use Prioritized Experience Replay", required = False, action = 'store_true')
            self.parser.add_argument("--noisy_net", help = "use Prioritized Experience Replay", required = False, action = 'store_true')
            self.parser.add_argument("--local_state", help = "define board size", required = False, action = 'store_true')
            self.parser.add_argument("--benchmark", help = "test the trained model", required = False, action = 'store_true')
            self.parser.add_argument("-n_steps", help = "choose the ammount of steps in Multi-step returns", required = False, default = 1, type = int)
            self.parser.add_argument("-board_size", help = "define board size", required = False, default = 10, type = int)
            self.parser.add_argument("-memory_size", help = "define the ammount of episodes to remember", required = False, default = -1, type = int)
            self.parser.add_argument("-nb_frames", help = "define board size", required = False, default = 4, type = int)
            self.parser.add_argument("-update_freq", help = "frequency to update target", required = False, default = 500, type = int)

            self.args = self.parser.parse_args() # Receive arguments


def model_name(model_type, double, dueling, n_steps, per, noisy):
    model_name = 'model_type'

    if double:
        model_name += '_double'
    if dueling:
        model_name += '_dueling'
    if per:
        model_name += '_per'
    if noisy:
        model_name += '_noisy'

    model_name += '_' + str(n_steps) + 'steps'
    model_name += '.h5'

    return model_name
