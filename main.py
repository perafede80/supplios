from run_simulation import simulate
from constants import Status


simulate(user_type=Status.GUEST_USER, payment_outcome=Status.SUCCESSFUL)
simulate(user_type=Status.GUEST_USER, payment_outcome=Status.FAILED)
simulate(user_type=Status.REGISTERED_USER, payment_outcome=Status.SUCCESSFUL)
simulate(user_type=Status.REGISTERED_USER, payment_outcome=Status.FAILED)
