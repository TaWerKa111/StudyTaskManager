import React from 'react'
import {forEach} from "react-bootstrap/ElementChildren";

const WorkDetail = ({work_details, name}) => {
    const complitedStage = (is_comp) =>
    {
        if (is_comp)
            return 'Да'
        return 'Нет'
    }

    let child_works = []

    work_details.forEach(function (work)
    {
        if (work.child){
            work.child.forEach(function (child){
                child_works.push(child)
            })
        }
    });

    let all_works = work_details.concat(child_works);

    if (work_details.length <= 0) {
        return (<h2 className='text-center'>Для загрузки работы нажмите на кнопку!</h2>)
    }
    else
        return (
            <div className='row'>
                <h1 className='text-center'>Этапы работы с названием {name}</h1>
                <table className='table'>
                    <tr className='d-md-table-row'>
                        <td>Идентификатор работы</td>
                        <td>Название этапа</td>
                        <td>Выполнен ли этап</td>
                        <td>Планируемая дата сдачи этапа</td>
                        <td>Дата сдачи этапа</td>
                    </tr>
                    {all_works.map(work =>
                        <tr className='d-md-table-row'>
                            <td>{work.academic_work_id}</td>
                            <td>{work.name}</td>
                            <td>{complitedStage(work.is_pass)}</td>
                            <td>{work.planned_date}</td>
                            <td>{work.actually_date}</td>
                        </tr>)}
                </table>
            </div>
        )
}

export default WorkDetail
