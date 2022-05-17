import React from 'react'

const TemplateList = ({templates}) => {
    return (
        <div className='container'>
            <div className='row'>
                <div className='col'>
                    <h1>Шаблоны для преподавателя</h1>
                    <table className='table'>
                    <tr className='d-md-table-row'>
                        <td>Идентификатор шаблона</td>
                        <td>Название шаблона</td>
                    </tr>
                    {templates.map(template =>
                        <tr className='d-md-table-row'>
                            <td>{template.template_id}</td>
                            <td>{template.name}</td>
                        </tr>)}
                </table>
                </div>
            </div>

        </div>
    )
}
export default TemplateList
