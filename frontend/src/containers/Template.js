import React, {Component, useState} from 'react';
import axios from "axios";
import {useNavigate, useParams} from "react-router-dom";
import TemplateList from "../Objects/TemplatesList";

const MAIN_URL = 'http://127.0.0.1:8000';


// class Template extends Component {
//
//     state = {
//         tempaltes: []
//     }
//
//     load_templates() {
//         const params = useParams();
//         const idTeacher = params.id;
//         let url1 = MAIN_URL + `/teach/api/templates/${idTeacher}/`
//         console.log(`url1 = ${url1.toString()}`)
//         axios.get(url1)
//         .then(response => {
//             this.setState({templates: response.data})
//         })
//         .catch(e => console.log(e))
//         Template.state.tempaltes = templates;
//     }
//
//     render() {
//         this.load_templates()
//         return (
//         <div className='container'>
//             <div className='row'>
//                 <div className='col'>
//                     <h1 className='text-center' style={{ margin: '10px'}}>Шаблоны для преподавателя</h1>
//                     <p>{JSON.stringify(this.state.tempaltes)}</p>
//                 </div>
//             </div>
//         </div>
//     )
//     }
// }

const Template = () => {

    const [idTemplate, setIdTemplate] = useState('');

    const onChangeIdTemplate = e => setIdTemplate(e.target.value);
    const navigate = useNavigate();
    const goToDetailTemplate = () => {
        navigate(`/template_detail/${idTemplate}`);
    }

    const [templates, setTemplates] = useState([])
    const params = useParams();
    const idTeacher = params.id;

    const load_templates =() => {
        let url1 = MAIN_URL + `/teach/api/templates/${idTeacher}/`
        console.log(`url1 = ${url1.toString()}`)
        axios.get(url1)
        .then(response => {
            setTemplates(response.data)
        })
        .catch(e => console.log(e))
        console.log(templates)
    }

    load_templates();

    return (
        <div className='container'>
            <div className='row justify-content-md-center form-template'>
                <div className='col-md'>
                    <div className='form-group'>
                    <input type={'text'}
                    name='idTemplate'
                    value={idTemplate}
                    onChange={e => onChangeIdTemplate(e)}
                    placeholder={'Введите id шаблона'}/>
                    <button className='btn btn-primary' onClick={goToDetailTemplate}>Посмотреть детали шаблона!</button>
                </div>
                </div>
            </div>
            <div className='row'>
                <div className='col'>
                    <h1 className='text-center' style={{ margin: '10px'}}>Шаблоны для преподавателя</h1>
                    <TemplateList templates={templates}/>
                </div>
            </div>
        </div>
    )
};

export default Template;
