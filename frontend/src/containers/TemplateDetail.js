import React, {useState} from 'react';
import {useParams} from "react-router-dom";
import axios from "axios";
import DetailTemp from "../Objects/DetailTemp";


const MAIN_URL = 'http://127.0.0.1:8000';


const TemplateDetail = () => {
    const params = useParams();
    let idTemplate = params.id;

    const [tempDet, setTemplateDetail] = useState([])
    const [status, setStatus] = useState()

    // Загрузка данные о шаблоне с сервера
    const fetchQuotes = () => {
      // this.setState({...this.state, isFetching: true})
        var url1 = MAIN_URL + `/teach/api/template-${idTemplate}/`
        console.log(`url1 = ${url1.toString()}`)
        axios.get(url1)
        .then(response => {
            setTemplateDetail(response.data)
        })
        .catch(e => console.log(e))
        console.log(tempDet)
    }

    return (
        <div className="container">
            <div className='row form-template'>
                <div className='col-md-auto'>
                    <label>Идентификатор шаблона = { idTemplate }</label>
                    <button className='btn btn-primary' onClick={fetchQuotes}>Загрузить данные!</button>
                </div>
            </div>
            <DetailTemp template_details={tempDet}/>
        </div>
    );
};

export default TemplateDetail;
