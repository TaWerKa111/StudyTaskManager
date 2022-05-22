import React, {useState} from 'react';
import {useParams} from "react-router-dom";
import WorkDetail from "../Objects/WorkDetail";
import axios from "axios";
const MAIN_URL = 'http://127.0.0.1:8000';

const StudyWork = ( { } ) => {
    const params = useParams();
    let name1 = params.name;
    console.log(name1)

    const [workDetail, setWorkList] = useState([])

    // Загрузка данных с сервера
    const fetchQuotes = () => {
      // this.setState({...this.state, isFetching: true})
        var url1 = MAIN_URL + `/teach/api/academs/${name1}/`
        console.log(`url1 = ${url1.toString()}`)
        axios.get(url1)
        .then(response => {
            setWorkList(response.data)
        })
        .catch(e => console.log(e))
    }

    return (
        <div className="container">
            StudyWork, { name1 }
            <button onClick={fetchQuotes}>Загрузить данные!</button>
            <div>
                <WorkDetail work_details={workDetail} name={''}/>
            </div>
        </div>

    );
};

export default StudyWork;
