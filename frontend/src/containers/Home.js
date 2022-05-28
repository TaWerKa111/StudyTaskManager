import React, {useState} from 'react';
import Form from 'react-bootstrap/Form'
import {FormControl, FormLabel} from "react-bootstrap";
import {Navigate, useNavigate} from "react-router-dom";
import axios from "axios";
import WorkList from "../Objects/WorkList"
import Select from "react-select";
// import '../style/main.css'

const MAIN_URL = 'http://127.0.0.1:8000';

const options = [
    {
        label: 'Ничего не выбрано',
        value: ''
    },
]

// Выполнена ли учебная работа
const opt_is_complited = [
    {
        label: 'Ничего не выбрано',
        value: ''
    },
    {
        label: 'Работа выполнена',
        value: 'Yes'
    },
    {
        label: 'Работа не выполнена',
        value: 'No'
    },
]

const Home = () => {
    // Для выборки
    const [isComplited, setIsComplited] = useState('')

    const getComplitedValue = () => {
        return isComplited ? opt_is_complited.find(c => c.value === isComplited) : ''
    }

    const onChangeIsComplited = (newValue) => {
        setIsComplited(newValue.value)
    }

    const [disciplineOptions, setDisciplineOptions] = useState(options)

    const getDisciplineValue = () => {
        return discipline ? disciplineOptions.find(c => c.value === discipline) : ''
    }

    const onChangeDiscipline = (newValue) => {
        setDiscipline(newValue.value)
    }

    const [formOfControlOptions, setFormOfControlOptions] = useState(options)

    const getFormOfControlValue = () => {
        return formOfControl ? formOfControlOptions.find(c => c.value === formOfControl) : ''
    }

    const onChangeFormOfControl= (newValue) => {
        setFormOfControl(newValue.value)
        let formOfControl = newValue.value

        if (formOfControl === '') {
            console.log(studyWorks)
            setFilterStudyWorks(studyWorks)
            return null
        }

        let temp = []
        if (filterStudyWorks) {
            filterStudyWorks.forEach(
                function (studyWork) {
                    if (studyWork.form_of_control_id.form_of_control_id === formOfControl){
                        temp.push(studyWork)
                    }
                }
            )

        }
        else {
            studyWorks.forEach(
                function (studyWork){
                    if (studyWork.form_of_control_id.form_of_control_id === formOfControl){
                        temp.push(studyWork)
                    }
            })

        }

        setFilterStudyWorks(temp)

    }

    const [discipline, setDiscipline] = useState('')
    const [formOfControl, setFormOfControl] = useState('')

    // Необходимые при работе программы
    const [idTeacher, setIdTeacher] = useState('');
    const [name, setName] = useState('');

    const [studyWorks, setStudyWorks] = useState([]);
    const [filterStudyWorks, setFilterStudyWorks] = useState([]);

    const onChangeIdTeacher = e => setIdTeacher(e.target.value);

    const onChangeName = (e) => {
        setName(e.target.value)

        let temp = []

        studyWorks.forEach(
            function (work){
                if (work.name.includes(e.target.value)){
                    temp.push(work)
                }
            }
        )

        setFilterStudyWorks(temp)

    }

    const setDisciplineOptionsFunc = (disciplineList) => {
        let newOptions = []
        Object.assign(newOptions, options)

        disciplineList.forEach(
            function (discipline) {
                newOptions.push({
                    label: discipline.name,
                    value: discipline.discipline_id,
                })
            }
        )

        setDisciplineOptions(newOptions)
    }

    const setFormOfControlFunc = (formOfControlList) => {
        let newOptions = []
        Object.assign(newOptions, options)
        formOfControlList.forEach(
            function (formOfControl) {
                newOptions.push(
                    {
                        label: formOfControl.name,
                        value: formOfControl.form_of_control_id,
                    }
                )
            }
        )
        setFormOfControlOptions(newOptions)
    }

    const getStudyWorks = () => {
        let url1 = MAIN_URL + `/teach/api/academs-${idTeacher}/`
        console.log(`url1 = ${url1.toString()}`)
        axios.get(url1)
        .then(response => {
            setFilterStudyWorks(response.data)
        })
        .catch(e => console.log(e))
        setStudyWorks(filterStudyWorks);

        console.log("Study work = ", studyWorks);

        axios.get(MAIN_URL + '/teach/api/disc/')
            .then(response => setDisciplineOptionsFunc(response.data))
            .catch(e => console.log(e))

        axios.get(MAIN_URL + '/teach/api/control/')
            .then(response => setFormOfControlFunc(response.data))
            .catch(e => console.log(e))

    }


    console.log('Дисциплина', discipline)
    console.log('Форма контроля', formOfControl)

    return(
        <div className='container main-content'>
            <div className='row'>
                <div className='col-md'>
                    <div className=' form-control element-form'>
                        <div className='form-group'>
                        <label>Введите id преподавателя: </label>
                        <input type={"text"}
                            name={'idTeacher'}
                            value={idTeacher}
                            onChange={e => onChangeIdTeacher(e)}
                        /></div>
                    <button className='btn btn-primary' type='submit' onClick={getStudyWorks}>Загрузить работы</button>
                    </div>
                </div>
            </div>
            <div className='row'>
                <div className='col-md'>
                    <div className='form-control element-form'>
                        <div className='form-group'>
                            <div className='input-group mb-3'>
                                <div className='input-group-prepend'>
                                    <span className='input-group-text'>Введите название работы</span>
                                </div>
                            <input type={"text"}
                                name={"name"}
                                value={name}
                                className=''
                                aria-describedby="basic-addon1"
                                onChange={e => onChangeName(e)}
                            />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div className='row'>
                <div className='col-md'>
                   <div className='form-control element-form'>
                        <div className='form-group'>
                            <Select placeholder='Форма контроля' onChange={onChangeFormOfControl}
                                    value={getFormOfControlValue()} options={formOfControlOptions}/>
                        </div>
                   </div>
                </div>
                <div className='col-md'>
                   <div className='form-control element-form'>
                        <div className='form-group'>
                            <Select placeholder='Дисциплина' onChange={onChangeDiscipline}
                                    value={getDisciplineValue()} options={disciplineOptions}/>
                        </div>
                   </div>
                </div>
                <div className='col-md'>
                   <div className='form-control element-form'>
                        <div className='form-group'>
                            <Select placeholder='Выполнена ли работа' onChange={onChangeIsComplited}
                                    value={getComplitedValue()} options={opt_is_complited}/>
                        </div>
                   </div>
                </div>
            </div>

            <WorkList work_list={filterStudyWorks}/>
        </div>
    )
};

export default Home;
