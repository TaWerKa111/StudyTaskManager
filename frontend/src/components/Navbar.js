import React from 'react';
import {useNavigate} from "react-router-dom";
import '../style/main.css'

const Navbar = () => {
    const divStyle = {
        color: '#9A7EA6',
        backgroundColor: '#42373D'
    }

    const aStyle = {
        textDecoration: 'none',
        color: '#9A7EA6',
    }

    return (<div className='container' style={divStyle}>
        <div className='row navbar'>
            <div className='col'>
                <a href='/' style={aStyle}><h2>Главное меню</h2></a>
            </div>
            <div className='col'>
                <a href='/templates/' style={aStyle}><h2>Шаблоны</h2></a>
            </div>
        </div>

    </div>
    )
};

export default Navbar;
