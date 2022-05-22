import React from 'react'
import {useNavigate} from "react-router-dom";

const TemplateList = ({templates}) => {
    const navigate = useNavigate();

    const goToDetailTemp = (e) => {
        const row= e.target.parentNode
        const rowText = row.innerText
        const idTemplate = rowText.split('\t')[0]

        console.log(idTemplate)

        navigate(`/template_detail/${idTemplate}`);
    }

    return (
        <div className='container'>
            <div className='row'>
                <div className='col'>
                    {/*<h1>Шаблоны для преподавателя</h1>*/}
                    <table className='table'>
                    <tr className='d-md-table-row'>
                        <td>Идентификатор шаблона</td>
                        <td>Название шаблона</td>
                    </tr>
                    {templates.map(template =>
                        <tr className='d-md-table-row work-row'
                        onClick={e => goToDetailTemp(e)}>
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
