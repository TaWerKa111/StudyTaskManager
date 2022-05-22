import React, {Component, useState} from 'react';
import {BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Home from './containers/Home'
import Template from './containers/Template'
import StudyWork from "./containers/StudyWork";
import CreateTemp from "./containers/CreateTemp";
import Activate from "./containers/Activate";
import Login from "./containers/Login";
import Layout from "./hocs/Layout";
import TemplateDetail from "./containers/TemplateDetail";

import {Provider } from 'react-redux';
import store from './store';
import './style/main.css';
import {render} from "react-dom";

// const MAIN_URL = 'http://0.0.0.0:8000';
// const MAIN_URL = 'http://localhost:8000';
const MAIN_URL = 'http://127.0.0.1:8000';

class App extends Component {
    constructor(props) {
        super(props);
        this.name = ""
    }


    handleNameChange = (name) =>{
        this.name = name
        console.log(`Имя изменилось! ${this.name}`)
    }

    render() {
        return (
            <Provider store={store}>
                <Router>
                    <Layout>
                        <Routes>
                            <Route exact path="/" element={<Home/>}/>
                            <Route exact path="/templates/:id/" element={<Template name={this.name}/>}/>
                            <Route exact path="/template_detail/:id/" element={<TemplateDetail/>}/>
                            <Route exact path="/study_work/:name/" element={<StudyWork/>}/>
                            <Route exact path="/create_template/" element={<CreateTemp/>}/>
                            {/*<Route exact path='/login' element={<Login/>} />*/}
                            {/*<Route exact path='/activate' element={<Activate/>} />*/}
                        </Routes>
                    </Layout>
                </Router>
            </Provider>
        )
    }
}

// const App = () => {
//
//
//
// };

// export default class App;
export default App;