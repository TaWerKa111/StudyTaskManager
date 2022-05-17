import React, {useState} from 'react';
import Form from 'react-bootstrap/Form'
import {FormControl, FormLabel} from "react-bootstrap";
import {Navigate, useNavigate} from "react-router-dom";
import axios from "axios";
import WorkList from "../Objects/WorkList"

const MAIN_URL = 'http://127.0.0.1:8000';

const Home = ( { onChange } ) => {
    const handleNameChange = () => {
        console.log(name);
        onChange(name);
    }

    const [name, setName] = useState('');
    const [idTeacher, setIdTeacher] = useState('');
    const [studyWorks, setStudyWorks] = useState([]);

    const onChange1 = e => setName(e.target.value);//setFormData({...formData, [e.target.name]: e.target.value});
    const onChangeIdTeacher = e => setIdTeacher(e.target.value);

    // Для навигации между страницами используется navigate
    const navigate = useNavigate();

    const goToStudy = () => {
        // if (name !== '') return <Navigate replace={true} to="/"/>;
        navigate(`/study_work/${name}`);
    }

    const getStudyWorks = () => {
        let url1 = MAIN_URL + `/teach/api/academs-${idTeacher}/`
        console.log(`url1 = ${url1.toString()}`)
      axios.get(url1)
        .then(response => {
            setStudyWorks(response.data)
        })
        .catch(e => console.log(e))
    console.log(studyWorks);
        onChange(idTeacher);
    }

    return(
        <div className='container'>
            <div className='row'>
                <div className='col-md'>
                    <form className='form-control element-form' onSubmit={handleNameChange}>
                        <div className='form-group'>
                            <label>Введите id учебной работы:  </label>
                            <input type={"text"}
                                name={'name'}
                                value={name}
                                onChange={e => onChange1(e)}
                            /></div>
                        <button className='btn btn-primary' type='submit' onClick={goToStudy}>Перейти на страницу работы</button>
                    </form>
                </div>
            </div>
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
            <WorkList work_list={studyWorks}/>

        </div>
    )
};

export default Home;
