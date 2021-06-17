
from rlbench.environment import Environment
from rlbench.action_modes import ArmActionMode, ActionMode
from rlbench.observation_config import ObservationConfig
from rlbench.tasks import ReachTarget
from rlbench.tasks import *
from rlbench.tasks import PickUpCup

import numpy as np


class ImitationLearning(object):

    def predict_action(self, batch):
        return np.random.uniform(size=(len(batch), 7))

    def behaviour_cloning_loss(self, ground_truth_actions, predicted_actions):
        return 1


# To use 'saved' demos, set the path below, and set live_demos=False
live_demos = True
DATASET = '' if live_demos else 'PATH/TO/YOUR/DATASET'

obs_config = ObservationConfig()
obs_config.set_all(True)

action_mode = ActionMode(ArmActionMode.ABS_JOINT_VELOCITY)
env = Environment(
    action_mode, DATASET, obs_config, False,
    robot_configuration='ur10_suction')
env.launch()
# task = env.get_task(ReachTarget)
task = env.get_task(PickUpCup)
# il = ImitationLearning()

demos = task.get_demos(2, live_demos=live_demos)  # -> List[List[Observation]]
demos = np.array(demos).flatten()
exit()
# An example of using the demos to 'train' using behaviour cloning loss.
for i in range(100):
    print("'training' iteration %d" % i)
    batch = np.random.choice(demos, replace=False)
    batch_images = [obs.left_shoulder_rgb for obs in batch]
    predicted_actions = il.predict_action(batch_images)
    ground_truth_actions = [obs.joint_velocities for obs in batch]
    loss = il.behaviour_cloning_loss(ground_truth_actions, predicted_actions)

print('Done')
env.shutdown()
