import React, {useState} from 'react'
import {useNavigate} from "react-router-dom";

const WorkList = ({work_list}) => {
    const complitedWork = (is_comp) =>
    {
        if (is_comp)
            return 'Выполнена'
        return 'Не выполнена'
    }

    const onHover = (e) => {
        const row= e.target.parentNode
        const rowText = row.innerText
        const idWork = rowText.split('\t')[0]
        navigate(`/study_work/${idWork}`);
    }

    const navigate = useNavigate();

    if (work_list.length <= 0 || work_list.result === false) {
        return (<h2 className='text-center'>Работы на найдены</h2>)
    }
    else
        return (
            <div className='row'>
                <h1 className='text-center'>Список работ для преподавателя</h1>
                <table className='table'>
                    <tr className='d-md-table-row'>
                        <td>Идентификатор работы</td>
                        <td>Название работы</td>
                        <td>Дисциплина</td>
                        <td>Форма контроля</td>
                        <td>Выполнена ли работа</td>
                        <td>Студент</td>
                    </tr>
                    {work_list.map(work =>
                        <tr className='d-md-table-row work-row'
                            onClick={e => onHover(e)}>
                            <td>{work.academic_work_id}</td>
                            <td>{work.name}</td>
                            <td>{work.discipline_id.name}</td>
                            <td>{work.form_of_control_id.name}</td>
                            <td>{complitedWork(work.is_complited)}</td>
                            <td>{work.student_id.user.first_name} {work.student_id.user.last_name}</td>
                        </tr>)}
                </table>
            </div>
        )
}

export default WorkList
