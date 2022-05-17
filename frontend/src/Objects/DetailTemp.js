import React from 'react'

const DetailTemp = ({template_details}) => {
    let child_stages = []

    if (template_details.length <= 0) {
        return (<h2 className='text-center'>Для загрузки шаблона нажмите на кнопку!</h2>)
    }
    else
        template_details.stages.forEach(function (stage)
        {
            if (stage.childs){
                stage.childs.forEach(function (child){
                    child_stages.push(child)
                })
            }
        });

        let all_stages = template_details.stages.concat(child_stages);
        return (
            <div className='row'>
                <h1 className='text-center'>Этапы шаблона с названием {template_details.name}</h1>
                <table className='table'>
                    <tr className='d-md-table-row'>
                        <td>Идентификатор этапа</td>
                        <td>Название этапа</td>
                        <td>Продолжительность этапа</td>
                    </tr>
                    {all_stages.map(stage =>
                        <tr className='d-md-table-row'>
                            <td>{stage.stage_id}</td>
                            <td>{stage.name}</td>
                            <td>{stage.duration}</td>
                        </tr>)}
                </table>
            </div>
        )
}

export default DetailTemp
