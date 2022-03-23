import React from 'react';
import {BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Home from './containers/Home'
import Activate from "./containers/Activate";
import Login from "./containers/Login";
import Layout from "./hocs/Layout";

import {Provider } from 'react-redux';
import store from './store';


const App = () => (
        <Provider store={store}>
            <Router>
                <Layout>
                    <Routes>
                        <Route exact path="/" element={<Home/>} />
                        <Route exact path='/login' element={<Login/>} />
                        <Route exact path='/activate' element={<Activate/>} />
                    </Routes>
                </Layout>
            </Router>
        </Provider>
);

export default App;