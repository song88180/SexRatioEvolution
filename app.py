from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
from Simulation import Simulation

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
stop_flag = True
pause_flag = False
restart_flag = False
extinct_flag = False
connected_flag = False
simulation = None

control_panel_dict = {
    'Primary_reproduction_rate': {
        'options': {'switch': False},
        'params': {
            'Primary_reproduction_rate_with_age_male': {
                'type': 'list',
                'min': 0,
                'max': 1,
                'step': 0.01,
                'explanation': "Controls the proportion of males that are willing to reproduce without other effects"
            },
            'Primary_reproduction_rate_with_age_female': {
                'type': 'list',
                'min': 0,
                'max': 1,
                'step': 0.01,
                'explanation': "Controls the proportion of females that are willing to reproduce without other effects"
            },
        },
    },
    'Primary_mortality': {
        'options': {'switch': False},
        'params': {
            'Primary_mortality_with_age_male': {
                'type': 'list',
                'min': 0,
                'max': 1,
                'step': 0.01,
                'explanation': "Controls the proportion of males will die without other effects"
            },
            'Primary_mortality_with_age_female': {
                'type': 'list',
                'min': 0,
                'max': 1,
                'step': 0.01,
                'explanation': "Controls the proportion of females will die without other effects"
            },
        },
    },
    'Population_growth': {
        'options': {'switch': True},
        'params': {
            'MORTALITY_COEFFICIENT': {
                'type': 'value',
                'min': -1E-12,
                'max': 10E-12,
                'step': 5E-13,
                'explanation':
                    """
                    Negative feedback on population growth, controls population saturation, like K in logistic model.\n
                    Survivorship = Primary_survivorship * (1 - MORTALITY_COEFFICIENT * Population_size)
                    """
            },
        },
    },
    'Parental_investment': {
        'options': {'switch': True},
        'params': {
            'PI_son_coef': {
                'type': 'list',
                'min': -1,
                'max': 1,
                'step': 0.01,
                'explanation': "Effect of having a son on parents' survivorship, stackable"
            },
            'PI_daughter_coef': {
                'type': 'list',
                'min': -1,
                'max': 1,
                'step': 0.01,
                'explanation': "Effect of having a daughter on parents' survivorship, stackable"
            },
        },
    },
    'Parental_care': {
        'options': {'switch': True},
        'params': {
            'Father_coef': {
                'type': 'value',
                'min': -1,
                'max': 1,
                'step': 0.01,
                'explanation': "Effect on one's survivorship if his/her father is not dead"
            },
            'Mother_coef': {
                'type': 'value',
                'min': -1,
                'max': 1,
                'step': 0.01,
                'explanation': "Effect on one's survivorship if his/her mother is not dead"
            },
        }
    },
    'Mating_willingness': {
        'options': {'switch': True},
        'params': {
            'MW_son_coef': {
                'type': 'value',
                'min': -1,
                'max': 1,
                'step': 0.01,
                'explanation': "Effect of having a son on parents' mating willingness, stackable"
            },
            'MW_daughter_coef': {
                'type': 'value',
                'min': -1,
                'max': 1,
                'step': 0.01,
                'explanation': "Effect of having a daughter on parents' mating willingness, stackable"
            },
        },
    },
    'Sibling_effect': {
        'options': {'switch': True},
        'params': {
            'Bro_coef': {
                'type': 'value',
                'min': -1,
                'max': 1,
                'step': 0.01,
                'explanation': "Effect of having a brother on one's survivorship, stackable"
            },
            'Sis_coef': {
                'type': 'value',
                'min': -1,
                'max': 1,
                'step': 0.01,
                'explanation': "Effect of having a sister on one's survivorship, stackable"
            },
        },
    },
}


@app.route('/')
def hello_world():
    global control_panel_dict
    global simulation
    global connected_flag
    if connected_flag:
        return """Sorry, we do not support multiple clients currently.<br>
        It seems someone else is using it right now.<br>
        Please try after a few minutes""", 403
    else:
        connected_flag = True
        return render_template("index.html", control_panel_dict=control_panel_dict)

@socketio.on('my_event')
def my_event():
    global simulation
    simulation = Simulation()
    simulation.reset()
    emit('load_settings', simulation.argv)
    run_simulation()

@socketio.on('change_param')
def change_param(data):
    global simulation
    print(data['param_name'])
    print(data['value'])
    simulation.argv[data['param_name']] = data['value']

@socketio.on('change_age_param')
def change_age_param(data):
    global simulation
    print(data['param_name'])
    print(data['age'])
    print(data['value'])
    simulation.argv[data['param_name']][data['age']] = data['value']

@socketio.on('change_all_age_param')
def change_all_age_param(data):
    global simulation
    print(data['param_name'])
    print('all')
    print(data['value'])
    start = 0
    end = 11
    if "Primary_reproduction_rate_with_age" in data['param_name']:
        start = 1
    elif "Primary_mortality_with_age" in data['param_name']:
        end = 10
    for age in range(start, end):
        simulation.argv[data['param_name']][age] = data['value']
    # for key in simulation.argv[data['param_name']].keys():
    #     simulation.argv[data['param_name']][key] = data['value']

@socketio.on('set_male_female_same')
def set_male_female_same(data):
    global simulation
    print('set_male_female_same')
    simulation.argv[data['param_name']] = simulation.argv[data['param_name_other_sex']].copy()


@socketio.on('run')
def run_simulation():
    global simulation
    global stop_flag
    global pause_flag
    global restart_flag
    global extinct_flag
    if not (stop_flag or pause_flag):
        print('Already running')
        return
    print('run simulation')
    if extinct_flag:
        emit('restart_finish')
        extinct_flag = False
    stop_flag = False
    pause_flag = False
    for i in range(20000):
        if stop_flag:
            simulation = None
            break
        elif pause_flag:
            emit('pause_finish')
            break
        elif restart_flag:
            emit('restart_finish')
            _argv_ = simulation.argv
            simulation = Simulation()
            simulation.reset()
            simulation.argv = _argv_
            restart_flag = False
        else:
            emit('run_finish')

        status = simulation.next_generation()
        if not status:
            _argv_ = simulation.argv
            simulation = Simulation()
            simulation.reset()
            simulation.argv = _argv_
            stop_flag = True
            extinct_flag = True
            emit('extinct')
            break

        emit_data = {
            'gen': simulation.Pop.Current_generation,
            'N_pop': simulation.N_list[-1],
            'N_sex_with_age': simulation.N_sex_with_age,
            'allele_append_dict': simulation.allele_append_dict,
            'sex_ratio': simulation.sex_ratio_list[-1],
            'sex_ratio_at_birth': simulation.sex_ratio_at_birth_list[-1],
            'max_age': simulation.Pop.max_age,
        }
        emit('message', emit_data)
        print(i)
    # if i == 20000-1:
    #     stop_flag = True

@socketio.on('pause')
def pause_simulation():
    global pause_flag
    print('pause_flag')
    pause_flag = True

@socketio.on('reset')
def reset_simulation():
    global simulation
    global pause_flag
    global stop_flag
    print('reset parameters')
    simulation.load_default_settings()
    emit('reset_finish')
    emit('load_settings', simulation.argv)

@socketio.on('restart')
def restart_simulation():
    global simulation
    global restart_flag
    restart_flag = True
    if stop_flag:
        run_simulation()


@socketio.on('disconnect')
def del_event():
    global stop_flag
    global connected_flag
    print('stop_flag')
    stop_flag = True
    connected_flag = False

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
