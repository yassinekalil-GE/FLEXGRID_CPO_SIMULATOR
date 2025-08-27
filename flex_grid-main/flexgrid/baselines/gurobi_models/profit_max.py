import numpy as np
import gurobipy as gp
from gurobipy import GRB
from gurobipy import *
import pickle


class V2GProfitMaxOracleGB():
    '''
    This file contains the EV_City_Math_Model class, which is used to solve the ev_city V2G problem optimally.
    '''
    algo_name = 'Optimal (Offline)'

    def __init__(self,
                 replay_path=None,
                 timelimit=None,
                 MIPGap=None,
                 verbose=True,
                 **kwargs):

        replay = pickle.load(open(replay_path, 'rb'))

        self.sim_length = replay.sim_length
        self.n_cs = replay.n_cs
        self.number_of_ports_per_cs = replay.max_n_ports
        self.n_transformers = replay.n_transformers
        self.timescale = replay.timescale
        dt = replay.timescale / 60  # time step
        print(f'\nGurobi MIQP solver for MO V2GPST.')
        print('Loading data...')

        tra_max_amps = replay.tra_max_amps
        tra_min_amps = replay.tra_min_amps
        cs_transformer = replay.cs_transformer
        port_max_charge_current = replay.port_max_charge_current
        port_min_charge_current = replay.port_min_charge_current
        port_max_discharge_current = replay.port_max_discharge_current
        port_min_discharge_current = replay.port_min_discharge_current
        voltages = replay.voltages / 1000  # phases included in voltage
        # phases = replay.phases

        charge_prices = replay.charge_prices  # Charge prices are in €/kWh
        discharge_prices = replay.discharge_prices  # Discharge prices are in €/kWh

        # power_setpoints = replay.power_setpoints

        cs_ch_efficiency = replay.cs_ch_efficiency *  0.9
        cs_dis_efficiency = replay.cs_dis_efficiency * 0.9
        
        ev_max_energy = replay.ev_max_energy
        
        ev_max_ch_power = replay.ev_max_ch_power  # * self.dt
        ev_max_dis_power = replay.ev_max_dis_power  # * self.dt
        ev_max_energy_at_departure = replay.max_energy_at_departure
        ev_des_energy = replay.ev_des_energy
        
        u = replay.u
        energy_at_arrival = replay.energy_at_arrival
        ev_arrival = replay.ev_arrival
        t_dep = replay.t_dep

        # create model
        print('Creating Gurobi model...')
        self.m = gp.Model("ev_city")
        # if verbose:
        #     self.m.setParam('OutputFlag', 1)
        # else:
        #     self.m.setParam('OutputFlag', 0)
        if MIPGap is not None:
            self.m.setParam('MIPGap', MIPGap)            
        if timelimit is not None:
            self.m.setParam('TimeLimit', timelimit)

        # energy of EVs t timeslot t
        energy = self.m.addVars(self.number_of_ports_per_cs,
                                self.n_cs,
                                self.sim_length,
                                vtype=GRB.CONTINUOUS,
                                name='energy')
                

        current_ev_dis = self.m.addVars(self.number_of_ports_per_cs,
                                        self.n_cs,
                                        self.sim_length,
                                        vtype=GRB.CONTINUOUS,
                                        name='current_ev_dis')
        current_ev_ch = self.m.addVars(self.number_of_ports_per_cs,
                                       self.n_cs,
                                       self.sim_length,
                                       vtype=GRB.CONTINUOUS,
                                       name='current_ev_ch')

        act_current_ev_dis = self.m.addVars(self.number_of_ports_per_cs,
                                            self.n_cs,
                                            self.sim_length,
                                            vtype=GRB.CONTINUOUS,
                                            name='act_current_ev_dis')
        act_current_ev_ch = self.m.addVars(self.number_of_ports_per_cs,
                                           self.n_cs,
                                           self.sim_length,
                                           vtype=GRB.CONTINUOUS,
                                           name='act_current_ev_ch')

        current_cs_ch = self.m.addVars(self.n_cs,
                                       self.sim_length,
                                       vtype=GRB.CONTINUOUS,
                                       name='current_cs_ch')

        current_cs_dis = self.m.addVars(self.n_cs,
                                        self.sim_length,
                                        vtype=GRB.CONTINUOUS,
                                        name='current_cs_dis')

        omega_ch = self.m.addVars(self.number_of_ports_per_cs,
                                  self.n_cs,
                                  self.sim_length,
                                  vtype=GRB.BINARY,
                                  name='omega_ch')
        omega_dis = self.m.addVars(self.number_of_ports_per_cs,
                                   self.n_cs,
                                   self.sim_length,
                                   vtype=GRB.BINARY,
                                   name='omega_dis')

        current_tr_ch = self.m.addVars(self.n_transformers,
                                       self.sim_length,
                                       vtype=GRB.CONTINUOUS,
                                       name='current_tr_ch')
        current_tr_dis = self.m.addVars(self.n_transformers,
                                        self.sim_length,
                                        vtype=GRB.CONTINUOUS,
                                        name='current_tr_dis')

        power_cs_ch = self.m.addVars(self.n_cs,
                                     self.sim_length,
                                     vtype=GRB.CONTINUOUS,
                                     name='power_cs_ch')

        power_cs_dis = self.m.addVars(self.n_cs,
                                      self.sim_length,
                                      vtype=GRB.CONTINUOUS,
                                      name='power_cs_dis')

        # power_error = self.m.addVars(self.sim_length,
        #                              vtype=GRB.CONTINUOUS,
        #                              name='power_error')

        total_power = self.m.addVars(self.sim_length,
                                     vtype=GRB.CONTINUOUS,
                                     name='total_power')

        power_tr_ch = self.m.addVars(self.n_transformers,
                                     self.sim_length,
                                     vtype=GRB.CONTINUOUS,
                                     name='power_tr_ch')

        power_tr_dis = self.m.addVars(self.n_transformers,
                                      self.sim_length,
                                      vtype=GRB.CONTINUOUS,
                                      name='power_tr_dis')

        is_exceeding_limit = self.m.addVars(self.sim_length,
                                            vtype=GRB.BINARY,
                                            name='is_exceeding_limit')
        
        user_satisfaction = self.m.addVars(self.number_of_ports_per_cs,
                                           self.n_cs,
                                           self.sim_length,
                                           vtype=GRB.CONTINUOUS,
                                           name='user_satisfaction')

        costs = self.m.addVar(vtype=GRB.CONTINUOUS,
                              name='total_soc')
        # Constrains
        # transformer current and power variables
        for t in range(self.sim_length):
            for i in range(self.n_transformers):
                self.m.addConstr(current_tr_ch[i, t] == gp.quicksum(current_cs_ch[m, t]
                                                                    for m in range(self.n_cs)
                                                                    if cs_transformer[m] == i))
                self.m.addConstr(current_tr_dis[i, t] == gp.quicksum(current_cs_dis[m, t]
                                                                     for m in range(self.n_cs)
                                                                     if cs_transformer[m] == i))

                self.m.addConstr(power_tr_ch[i, t] == gp.quicksum(power_cs_ch[m, t]
                                                                  for m in range(self.n_cs)
                                                                  if cs_transformer[m] == i),
                                 name=f'power_tr_ch.{i}.{t}')
                self.m.addConstr(power_tr_dis[i, t] == gp.quicksum(power_cs_dis[m, t]
                                                                   for m in range(self.n_cs)
                                                                   if cs_transformer[m] == i),
                                 name=f'power_tr_dis.{i}.{t}')

            self.m.addConstr(total_power[t] == gp.quicksum(power_tr_ch[i, t] - power_tr_dis[i, t]
                                                           for i in range(self.n_transformers)),
                             name=f'total_power.{t}')

            # M = 1e8
            # self.m.addConstr(power_error[t] >= total_power[t] - power_setpoints[t],
            #                  name=f'power_error_max.{t}')
            # self.m.addConstr(power_error[t] <= (total_power[t] - power_setpoints[t])* is_exceeding_limit[t],
            #                  name=f'power_error_min.{t}')
            # self.m.addConstr(power_error[t] <= 0,
            #                     name=f'power_error_min2.{t}')
            
            # self.m.addConstr(power_error[t] <= M * is_exceeding_limit[t],
            #                     name=f'power_error_max.{t}')
            # self.m.addConstr(power_error[t] >= 1-M * (1-is_exceeding_limit[t]),
            #                     name=f'power_error_max2.{t}')

            # add contraint for aggregated power limit
            # self.m.addConstr(total_power[t] <= power_setpoints[t],
            #                  name=f'total_power_limit_max.{t}')


        costs = gp.quicksum(act_current_ev_ch[p, i, t] * voltages[i] * cs_ch_efficiency[i, t] * dt * charge_prices[i, t] +
                            act_current_ev_dis[p, i, t] * voltages[i] *
                            cs_dis_efficiency[i, t] *
                            dt * discharge_prices[i, t]
                            for p in range(self.number_of_ports_per_cs)
                            for i in range(self.n_cs)
                            for t in range(self.sim_length))

        self.m.addConstrs(power_cs_ch[i, t] == (current_cs_ch[i, t] * voltages[i])
                          for i in range(self.n_cs)
                          for t in range(self.sim_length))
        self.m.addConstrs(power_cs_dis[i, t] == (current_cs_dis[i, t] * voltages[i])
                          for i in range(self.n_cs)
                          for t in range(self.sim_length))

        # transformer current output constraint (circuit breaker)
        self.m.addConstrs((current_tr_ch[i, t] - current_tr_dis[i, t] <= tra_max_amps[i, t]
                           for i in range(self.n_transformers)
                           for t in range(self.sim_length)), name='tr_current_limit_max')
        self.m.addConstrs((current_tr_ch[i, t] - current_tr_dis[i, t] >= tra_min_amps[i, t]
                           for i in range(self.n_transformers)
                           for t in range(self.sim_length)), name='tr_current_limit_min')

        # charging station total current output (sum of ports) constraint
        self.m.addConstrs((current_cs_ch[i, t] == act_current_ev_ch.sum('*', i, t)
                           for i in range(self.n_cs)
                           for t in range(self.sim_length)), name='cs_ch_current_output')
        self.m.addConstrs((current_cs_dis[i, t] == act_current_ev_dis.sum('*', i, t)
                           for i in range(self.n_cs)
                           for t in range(self.sim_length)), name='cs_dis_current_output')

        # charging station current output constraint
        self.m.addConstrs((-current_cs_dis[i, t] + current_cs_ch[i, t] >= port_max_discharge_current[i]
                           for i in range(self.n_cs)
                           for t in range(self.sim_length)), name='cs_current_dis_limit_max')
        self.m.addConstrs((-current_cs_dis[i, t] + current_cs_ch[i, t] <= port_max_charge_current[i]
                           for i in range(self.n_cs)
                           for t in range(self.sim_length)), name='cs_curent_ch_limit_max')

        self.m.addConstrs((act_current_ev_ch[p, i, t] == current_ev_ch[p, i, t] * omega_ch[p, i, t]
                           for p in range(self.number_of_ports_per_cs)
                           for i in range(self.n_cs)
                           for t in range(self.sim_length)
                           #    if u[p, i, t] == 1 and ev_arrival[p, i, t] == 0
                           ), name='act_ev_current_ch')

        self.m.addConstrs((act_current_ev_dis[p, i, t] == current_ev_dis[p, i, t] * omega_dis[p, i, t]
                           for p in range(self.number_of_ports_per_cs)
                           for i in range(self.n_cs)
                           for t in range(self.sim_length)
                           #    if u[p, i, t] == 1 and ev_arrival[p, i, t] == 0
                           ), name='act_ev_current_dis')

        # ev current output constraint
        self.m.addConstrs((current_ev_ch[p, i, t] >= port_min_charge_current[i]  # * omega_ch[p, i, t]
                           for p in range(self.number_of_ports_per_cs)
                           for i in range(self.n_cs)
                           for t in range(self.sim_length)
                           #    if u[p, i, t] == 1 and ev_arrival[p, i, t] == 0
                           ), name='ev_current_ch_limit_min')
        self.m.addConstrs((current_ev_dis[p, i, t] >= -port_min_discharge_current[i]  # * omega_dis[p, i, t]
                           for p in range(self.number_of_ports_per_cs)
                           for i in range(self.n_cs)
                           for t in range(self.sim_length)
                           #    if u[p, i, t] == 1 and ev_arrival[p, i, t] == 0
                           ), name='ev_current_dis_limit_min')

        # ev max charging current constraint
        self.m.addConstrs((current_ev_ch[p, i, t] <= min(ev_max_ch_power[p, i, t]/voltages[i], port_max_charge_current[i])
                           for p in range(self.number_of_ports_per_cs)
                           for i in range(self.n_cs)
                           for t in range(self.sim_length)
                           if u[p, i, t] == 1 and ev_arrival[p, i, t] == 0
                           ),
                          name='ev_current_ch_limit_max')

        # ev max discharging current constraint
        self.m.addConstrs((current_ev_dis[p, i, t] <= min(-ev_max_dis_power[p, i, t]/voltages[i], -port_max_discharge_current[i])
                           for p in range(self.number_of_ports_per_cs)
                           for i in range(self.n_cs)
                           for t in range(self.sim_length)
                           if u[p, i, t] == 1 and ev_arrival[p, i, t] == 0
                           ),
                          name='ev_current_dis_limit_max')

        # ev charge power if empty port constraint
        for t in range(self.sim_length):
            for i in range(self.n_cs):
                for p in range(self.number_of_ports_per_cs):
                    if u[p, i, t] == 0 or ev_arrival[p, i, t] == 1:
                        #     self.m.addLConstr((act_current_ev_ch[p, i, t] == 0),
                        #                       name=f'ev_empty_port_ch.{p}.{i}.{t}')
                        #     self.m.addLConstr((act_current_ev_dis[p, i, t] == 0),
                        #                       name=f'ev_empty_port_dis.{p}.{i}.{t}')

                        self.m.addLConstr((omega_ch[p, i, t] == 0),
                                          name=f'omega_empty_port_ch.{p}.{i}.{t}')
                        self.m.addLConstr((omega_dis[p, i, t] == 0),
                                          name=f'omega_empty_port_dis.{p}.{i}.{t}')

                    if u[p, i, t] == 0 and t_dep[p, i, t] == 0:
                        self.m.addLConstr(energy[p, i, t] == 0,
                                          name=f'ev_empty_port_energy.{p}.{i}.{t}')

        # energy of EVs after charge/discharge constraint
        for t in range(1, self.sim_length):
            for i in range(self.n_cs):
                for p in range(self.number_of_ports_per_cs):
                    if ev_arrival[p, i, t] == 1:
                        self.m.addLConstr(
                            energy[p, i, t] == energy_at_arrival[p, i, t],
                            name=f'ev_arrival_energy.{p}.{i}.{t}')

                    if u[p, i, t-1] == 1:
                        self.m.addConstr(energy[p, i, t] == (energy[p, i, t-1] +
                                                             act_current_ev_ch[p, i, t] * voltages[i] * cs_ch_efficiency[i, t] * dt -
                                                             act_current_ev_dis[p, i, t] * voltages[i] * cs_dis_efficiency[i, t] * dt),
                                         name=f'ev_energy.{p}.{i}.{t}')

        # energy level of EVs constraint
        self.m.addConstrs((energy[p, i, t] >= 0
                           for p in range(self.number_of_ports_per_cs)
                           for i in range(self.n_cs)
                           for t in range(self.sim_length)), name='ev_energy_level_min')
        self.m.addConstrs((energy[p, i, t] <= ev_max_energy[p, i, t]
                           for p in range(self.number_of_ports_per_cs)
                           for i in range(self.n_cs)
                           for t in range(self.sim_length)
                           if t_dep[p, i, t] != 1
                           ), name='ev_energy_level_max')

        # Power output of EVs constraint
        self.m.addConstrs((omega_dis[p, i, t] * omega_ch[p, i, t] == 0
                           for p in range(self.number_of_ports_per_cs)
                           for i in range(self.n_cs)
                           for t in range(self.sim_length)), name='ev_power_mode_2')

        # time of departure of EVs
        for t in range(self.sim_length):
            for i in range(self.n_cs):
                for p in range(self.number_of_ports_per_cs):
                    if t_dep[p, i, t] == 1:
                        
                        
                    #     self.m.addLConstr(energy[p, i, t] >= ev_max_energy_at_departure[p, i, t]-5,
                    #                       name=f'ev_departure_energy.{p}.{i}.{t}')
                        
                        self.m.addConstr(user_satisfaction[p, i, t] == \
                            (ev_des_energy[p, i, t] * ev_max_energy[p, i, t-1] - energy[p, i, t])**2,
                            name=f'ev_user_satisfaction.{p}.{i}.{t}')
                        
                        

        # self.m.setObjective(costs - 0.01*power_error.sum(),
        #                     GRB.MAXIMIZE)

        self.m.setObjective(costs - 100 * user_satisfaction.sum(),
                            GRB.MAXIMIZE)

        # print constraints
        self.m.write("model.lp")
        print(f'Optimizing...')
        self.m.params.NonConvex = 2

        self.m.optimize()

        self.act_current_ev_ch = act_current_ev_ch
        self.act_current_ev_dis = act_current_ev_dis
        self.port_max_charge_current = port_max_charge_current
        self.port_max_discharge_current = port_max_discharge_current

        if self.m.status != GRB.Status.OPTIMAL:
            print(f'Optimization ended with status {self.m.status}')
            # exit()

        self.get_actions()

    def get_actions(self):
        '''
        This function returns the actions of the EVs in the simulation normalized to [-1, 1]
        '''

        self.actions = np.zeros([self.number_of_ports_per_cs,
                                 self.n_cs, self.sim_length])

        for t in range(self.sim_length):
            for i in range(self.n_cs):
                for p in range(self.number_of_ports_per_cs):
                    if self.act_current_ev_ch[p, i, t].x > 0:
                        self.actions[p, i, t] = self.act_current_ev_ch[p, i, t].x  \
                            / self.port_max_charge_current[i]
                    elif self.act_current_ev_dis[p, i, t].x > 0:
                        self.actions[p, i, t] = self.act_current_ev_dis[p, i, t].x \
                            / self.port_max_discharge_current[i]

        return self.actions

    def get_action(self, env, **kwargs):
        '''
        This function returns the action for the current step of the environment.
        '''

        step = env.current_step

        return self.actions[:, :, step].T.reshape(-1)
