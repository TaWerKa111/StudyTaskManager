import React from 'react';

const Foot = () => {
    const divStyle = {
        color: '#9A7EA6',
        backgroundColor: '#42373D',
    }

    const aStyle = {
        textDecoration: 'none',
        color: '#9A7EA6',
    }

    return (
        <div className='fixed-bottom panel-footer' style={divStyle}>
        <div className='container'>
            <div className='row'>
                <div className='col-5'>
                    Copyright© 2022
                </div>
                <div className='col-5'>
                    <a href='https://t.me/gleb4lk' style={aStyle}>Telegram</a>
                </div>
            </div>
        </div>
    </div>
)
};

export default Foot;
