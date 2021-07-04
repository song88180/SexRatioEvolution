function selectColor(number) {
    const hue = number * 137.508; // use golden angle approximation
    return `hsl(${hue},50%,75%)`;
}

function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}

function clearData(chart){
    if (chart.config.type == 'line'){
        chart.data.labels = [];
        chart.data.datasets.forEach((dataset) => {
            dataset.data = [];
        })
    }
    else if (chart.config.type == 'scatter'){
        console.log('delete scatter chart')
        chart.data.labels = [];
        chart.data.datasets.forEach((dataset) => {
            dataset.data = [];
        })
    }
}

function updateAlleleChart(AlleleChart, allele_append_dict, gen) {
    let N_sum = 0;
    const allele_effect_dict = {
        0: 0,
        1: -0.2,
        2: -0.1,
        3: -0.05,
        4: -0.02,
        5: -0.01,
        6: 0.01,
        7: 0.02,
        8: 0.05,
        9: 0.1,
        10: 0.2,
    }
    for (const allele in allele_append_dict){
        N_sum += allele_append_dict[allele];
    }
    AlleleChart.data.datasets.forEach((dataset) => {
        if (dataset.label in allele_append_dict){
            dataset.data.push(
                {x:gen, y:allele_append_dict[dataset.label]/N_sum}
            );
            delete allele_append_dict[dataset.label];
        }
    });
    for (const allele in allele_append_dict){
        if (allele == 0){continue}
        _color_str_ = selectColor(parseInt(allele));
        AlleleChart.data.datasets.push(
            {
                label: allele,
                backgroundColor: _color_str_,
                borderColor: _color_str_,
                effect: allele_effect_dict[allele],
                data: [{x: gen, y: allele_append_dict[allele]/N_sum}]
            }
        )
    }
    AlleleChart.update();
}

function updateSexAgeChart(SexAgeChart, Male_list, Female_list) {
    SexAgeChart.data.datasets[0].data = Male_list;
    SexAgeChart.data.datasets[1].data = Female_list;
    SexAgeChart.update();
}

function updateSexRatioChart(SexRatioChart, sex_ratio, gen){
    SexRatioChart.data.labels.push(gen);
    SexRatioChart.data.datasets[0].data.push(sex_ratio);
    SexRatioChart.update();
}

function updateBirthSexRatioChart(BirthSexRatioChart, sex_ratio_at_birth, gen){
    BirthSexRatioChart.data.labels.push(gen);
    BirthSexRatioChart.data.datasets[0].data.push(sex_ratio_at_birth);
    BirthSexRatioChart.update();
}


var NPopChart = new Chart(
    $('#NPopChart'),
    {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Population size',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: [],
            }]
        },
        options: {
            responsive: false,
            animations: {
                y:{
                    duration: 0,
                }
            },
            plugins: {
                legend: {display: false},
                title:{
                    display: true,
                    text: "Whole population size",
                    font: {size: 20},
                }
            }
        }
    },
);

var SexAgeChart = new Chart(
    $('#SexAgeChart'),
    {
        type: 'line',
        data: {
            labels: Array.from({length: 10}, (_, i) => i + 1),
            datasets: [
                {
                    label: 'Male',
                    backgroundColor: 'rgb(15,76,246)',
                    borderColor: 'rgb(15,76,246)',
                    data: [],
                },
                {
                    label: 'Female',
                    backgroundColor: 'rgb(255, 99, 132)',
                    borderColor: 'rgb(255, 99, 132)',
                    data: [],
                }
            ]
        },
        options: {
            responsive: false,
            plugins: {
                title: {
                    display: true,
                    text: "Current population structure",
                    font: {size: 20},
                }
            }
        }
    },
);

var AlleleChart = new Chart(
    $('#AlleleChart'),
    {
        type: 'scatter',
        data: {
            datasets: []
        },
        options: {
            responsive: false,
            animations: {
                y:{
                    duration: 0,
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: "Allele frequency",
                    font: {size: 20},
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return "allele_" + context.label + ": " + context.dataset.effect;
                        }
                    }
                }

            }
        }
    },
);

var SexRatioChart = new Chart(
    $('#SexRatioChart'),
    {
        type: 'line',
        data: {
            datasets: [
                {
                    label: 'Sex_ratio',
                    backgroundColor: 'rgb(255, 99, 132)',
                    borderColor: 'rgb(255, 99, 132)',
                    data: [],
                    showLine: false,
                }
            ]
        },
        options: {
            responsive: false,
            animations: {
                y:{
                    duration: 0,
                }
            },
            plugins: {
                legend: {display: false},
                title: {
                    display: true,
                    text: "Sex ratio of whole population",
                    font: {size: 20},
                }
            }
        }
    },
);

var BirthSexRatioChart = new Chart(
    $('#BirthSexRatioChart'),
    {
        type: 'line',
        data: {
            datasets: [
                {
                    label: 'Sex_ratio_at_birth',
                    backgroundColor: 'rgb(255, 99, 132)',
                    borderColor: 'rgb(255, 99, 132)',
                    data: [],
                    showLine: false,
                }
            ]
        },
        options: {
            responsive: false,
            animations: {
                y:{
                    duration: 0,
                }
            },
            plugins: {
                legend: {display: false},
                title: {
                    display: true,
                    text: "Sex ratio at birth",
                    font: {size: 20},
                }
            }
        }
    },
);

function set_section(section_name, state_on){
    let section = document.getElementById(section_name);
    let toggle = section.getElementsByClassName('toggle')[0]
    if (toggle) {
        let slider_array = section.getElementsByClassName('slider');
        let section_body = document.getElementById(section_name + "_body");

        if (state_on) {
            toggle.checked = true;
            section_body.style.display = 'block';
            for (var index = 0; index < slider_array.length; index++) {
                slider_array[index].disabled = false;
            }
        } else {
            toggle.checked = false;
            section_body.style.display = 'none';
            for (var index = 0; index < slider_array.length; index++) {
                slider_array[index].disabled = true;
            }
        }
    }
}

function set_param(param_name, value){
    let slider = document.getElementById(param_name);
    let output = document.getElementById(param_name + "_value");
    slider.value = value;
    output.innerHTML = value;
}

function set_param_list(param_name, age_dict){
    for (const [age, value] of Object.entries(age_dict)) {
        let param_name_age = param_name + '_' + age;
        set_param(param_name_age, value);
    }
    if (param_name.includes("Primary_reproduction_rate_with_age")){
        let container = document.getElementById(param_name+"_0").parentElement;
        container.style.display="none";
    }else if (param_name.includes("Primary_mortality_with_age")){
        let slider = document.getElementById(param_name+"_10");
        slider.disabled=true;
    }
}

window.onload = function() {

    // Inline popups
    $('.inline-popups').magnificPopup({
      delegate: 'a',
      removalDelay: 500, //delay removal by X to allow out-animation
      callbacks: {
        beforeOpen: function() {
           this.st.mainClass = this.st.el.attr('data-effect');
        }
      },
      midClick: true // allow opening popup on middle mouse click. Always set it to true if you don't provide alternative source.
    });

    // initiate control-panel
    const section_toggle_array = ["Population_growth","Parental_investment",
                          "Parental_care","Mating_willingness","Sibling_effect"]
    const section_no_toggle_array = ["Primary_reproduction_rate","Primary_mortality"]
    const param_value_array = ["MORTALITY_COEFFICIENT","Father_coef","Mother_coef",
                               "MW_son_coef","MW_daughter_coef", "Bro_coef","Sis_coef"]
    const param_list_array = ["Primary_reproduction_rate_with_age_male","Primary_reproduction_rate_with_age_female",
                              "Primary_mortality_with_age_male","Primary_mortality_with_age_female",
                              "PI_son_coef","PI_daughter_coef"] // list of parameters for each age

    // set up socketio
    var socket = io.connect({port:5000, host: "0.0.0.0"});

    // once connected:
    socket.on('connect', function() {
        console.log('connected!!!');
        socket.emit('my_event');
    });

    // once simulation settings are loaded at the server side
    // initiate default parameters
    socket.on('load_settings',function(default_argv){
        section_toggle_array.forEach(section_name => {
            set_section(section_name, default_argv[section_name]);
        })
        param_value_array.forEach(param_name => {
            set_param(param_name, default_argv[param_name])
        })
        param_list_array.forEach(param_name => {
            set_param_list(param_name, default_argv[param_name])
        })
    })

    // once one step of the simulation is finished
    // update all charts
    socket.on('message', function(emit_data){
        addData(NPopChart, emit_data.gen, emit_data.N_pop);
        updateSexAgeChart(SexAgeChart, emit_data.N_sex_with_age.Male, emit_data.N_sex_with_age.Female);
        updateAlleleChart(AlleleChart, emit_data.allele_append_dict, emit_data.gen);
        updateSexRatioChart(SexRatioChart, emit_data.sex_ratio, emit_data.gen);
        updateBirthSexRatioChart(BirthSexRatioChart, emit_data.sex_ratio_at_birth, emit_data.gen);
    });

    // once disconnect
    // send message to server to let server stop running
    socket.on('disconnect', function(){
        socket.emit('disconnect')
    })


    // Add event listener to all value sliders
    param_value_array.forEach(function(param_name){
        let slider = document.getElementById(param_name);
        let output = document.getElementById(param_name + "_value");
        // Update the current slider value (each time you drag the slider handle)
        slider.oninput = function () {
            output.innerHTML = slider.value;
        }
        slider.onmouseup = function () {
            socket.emit('change_param', {param_name: param_name, value: parseFloat(slider.value)});
        }
    })

    // Add event listener to all age(list) sliders
    param_list_array.forEach(function(param_name){
        for (let age=0; age<11; age++){
            let param_name_age = param_name + '_' + age;
            let slider = document.getElementById(param_name_age);
            let output = document.getElementById(param_name_age + "_value");
            slider.oninput = function () {
                output.innerHTML = slider.value;
            }
            slider.onmouseup = function () {
                socket.emit('change_age_param', {param_name: param_name, age: age, value: parseFloat(slider.value)});
            }
        }

        let slider = document.getElementById(param_name + "_all");
        slider.oninput = function () {
            let start=0, end=11;
            if (param_name.includes("Primary_reproduction_rate_with_age")){start=1;}
            else if (param_name.includes("Primary_mortality_with_age")){end=10;}
            for (let age=start; age<end; age++){
                let param_name_age = param_name + '_' + age;
                let slider_age = document.getElementById(param_name_age);
                let output_age = document.getElementById(param_name_age + "_value");
                slider_age.value = slider.value;
                output_age.innerHTML = slider.value;
            }
        }
        slider.onmouseup = function () {
            socket.emit('change_all_age_param', {param_name: param_name, value: parseFloat(slider.value)});
        }

        let set_same_button = document.getElementById(param_name + "_set_same");
        set_same_button.onclick = function(){
            let param_name_other_sex
            if (param_name.includes("_male")){
                param_name_other_sex = param_name.replace("_male", "_female");
            }else if (param_name.includes("_female")){
                param_name_other_sex = param_name.replace("_female", "_male");
            }else if (param_name.includes("_son_")){
                param_name_other_sex = param_name.replace("_son_", "_daughter_");
            }else if (param_name.includes("_daughter_")){
                param_name_other_sex = param_name.replace("_daughter_", "_son_");
            }
            for (let age=0; age<11; age++){
                let param_name_age = param_name + '_' + age;
                let param_name_other_sex_age = param_name_other_sex + '_' + age;
                let slider_age = document.getElementById(param_name_age);
                let slider_other_sex_age = document.getElementById(param_name_other_sex_age)
                let output_age = document.getElementById(param_name_age + "_value");
                slider_age.value = slider_other_sex_age.value;
                output_age.innerHTML = slider_other_sex_age.value;
            }
            socket.emit('set_male_female_same',{param_name: param_name, param_name_other_sex: param_name_other_sex})
        }

    })

    section_toggle_array.forEach(function(section_name){
        let section = document.getElementById(section_name)
        let toggle = section.getElementsByClassName('toggle')[0]
        // Update the current toggle value (each time you drag the slider handle)
        toggle.onchange = function () {
            socket.emit('change_param', {param_name: section_name, value: toggle.checked});

            set_section(section_name, toggle.checked);
        }
    })

    const run_pause_btn = document.getElementById('run-pause-button');
    run_pause_btn.onclick = function() {
        if (run_pause_btn.value == 'pause'){
            socket.emit('pause');
            run_pause_btn.disabled = true;
        } else{
            socket.emit('run');
            run_pause_btn.disabled = true;
        }
    };

    socket.on('pause_finish', function(){
        run_pause_btn.disabled = false;
        run_pause_btn.value = 'run';
        run_pause_btn.innerHTML = 'Run!'
    })

    socket.on('run_finish', function(){
        run_pause_btn.disabled = false;
        run_pause_btn.value = 'pause';
        run_pause_btn.innerHTML = 'Pause!'
    })

    const restart_btn = document.getElementById('restart-button');
    restart_btn.onclick = function() {
        socket.emit('restart');
    };

    socket.on('restart_finish', function(){
        clearData(NPopChart);
        clearData(SexAgeChart);
        clearData(AlleleChart);
        clearData(SexRatioChart);
        clearData(BirthSexRatioChart);
        SexAgeChart.data.labels = Array.from({length: 10}, (_, i) => i + 1);
    })

    reset_btn = document.getElementById('reset-button');
    reset_btn.onclick = function() {
        socket.emit('reset');
        reset_btn.disabled=true;
    };

    socket.on('reset_finish', function(){
        reset_btn.disabled=false;
    })

    socket.on('extinct', function (){
        run_pause_btn.value = 'run';
        run_pause_btn.innerHTML = 'Run!';
    })
};