import React from 'react';
import Navbar from '../components/Navbar'
import Foot from '../components/Foot'

const Layout = (props) => (
    <div>
        <Navbar/>
        {props.children}
        <Foot/>
    </div>
);

export default Layout;
