def resize(io_vars, size):
  ## reshape??
  io_vars.pos.resize(2, size)
  io_vars.conf.resize(size)


def init_solver_vars(in_params, in_curve, initial_vars, solver_vars, update):

  if update:
    solver_vars.k = 0
    solver_vars.nu = 2.0
    solver_vars.j = 0
    solver_vars.epsilon = 1e-7

  elif solver_vars.x.pos.cols() != in_curve->n_vertices:
    resize(solver_vars.x, in_curve)
    resize(solver_vars.x, in_curve)

def secant_lm_method(in_params, in_curve, initial_vars, solver_vars, solution):

  init_solver_vars(in_params, in_curve, initial_vars, solver_vars)

  while True:
    if secant_lm_method_single_update(in_params, in_curve, initial_vars, solver_vars, solution):
      break
    update_curve_subdivision(in_params, initial_vars, solution, in_curve, sover_vars)


  solution = solver_vars.x

  show_feature_points(in_curve, solution)

