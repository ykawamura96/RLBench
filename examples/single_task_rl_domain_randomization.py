import numpy as np
from rlbench import (ArmActionMode, DomainRandomizationEnvironment,
                     ObservationConfig, RandomizeEvery)
from rlbench.action_modes import ActionMode
from rlbench.environment import Environment
from rlbench.sim2real.domain_randomization import DynamicsRandomizationConfig, VisualRandomizationConfig
from rlbench.tasks import PickUpCup


obs_config = ObservationConfig()
obs_config.set_all(True)

# To use 'saved' demos, set the path below, and set live_demos=False
live_demos = True
DATASET = '' if live_demos else 'PATH/TO/YOUR/DATASET'

# We will borrow some from the tests dir
rand_config = VisualRandomizationConfig(
    image_directory='../tests/unit/assets/textures')
dynamic_randomization_config = DynamicsRandomizationConfig(
    randomize_table_heigt=True,
    table_height_range=(-0.1, 0.1)
)
action_mode = ActionMode(ArmActionMode.ABS_JOINT_VELOCITY)
env = Environment(
    action_mode, obs_config=obs_config, headless=False,
    randomize_every=RandomizeEvery.EPISODE, frequency=1,
    robot_configuration='ur10_suction',
    visual_randomization_config=rand_config,
    dynamics_randomization_config=dynamic_randomization_config
)
env.launch()

task = env.get_task(PickUpCup)

demos = task.get_demos(2, live_demos=live_demos)  # -> List[List[Observation]]

print('Done')
env.shutdown()
