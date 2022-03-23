import React, {useState} from 'react';
import {Link, Redirect } from "react-router-dom";
import {connect} from 'react-redux';
import 'bootstrap/dist/css/bootstrap.min.css'
import {login} from '../actions/auth'

const Login = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: ''
    });

    const {email, password} = formData;

    const onChange = e => setFormData({...formData, [e.target.name]: e.target.value});


    const onSubmit = e => {
        e.preventDefault();
        login(email, password);
    };

    // is the user Authenticated&
    // redirect them on home page

    return (
        <div className='container mt-5 '>
            <h1>
                Sign in
            </h1>
            <p>Sign into your accounts</p>
            <form onSubmit={e => onSubmit(e)}>
                <div className='form-group '>
                    <input
                        className='form-control'
                        type='email'
                        placeholder='email'
                        name='email'
                        value={email}

                        onChange={e => onChange(e)}
                        required
                    />
                </div>
                <div className='form-group mt-2'>
                    <input
                        className='form-control'
                        type='password'
                        placeholder='password'
                        name='password'
                        value={password}
                        onChange={e => onChange(e)}
                        minLength={'6'}
                        required
                    />
                </div>
                <button className='btn btn-primary mt-2'  type='submit'>Войти</button>
            </form>
            <p className='mt-3'> Кек </p>
        </div>
    )
};

// const mapStateToProps = state => ({
//    // is authenticated?
//
//
//
// });


export default connect(null, {})(Login);