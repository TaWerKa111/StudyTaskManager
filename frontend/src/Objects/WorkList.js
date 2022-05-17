import React from 'react'

const WorkList = ({work_list}) => {

    const complitedWork = (is_comp) =>
    {
        if (is_comp)
            return 'Выполнена'
        return 'Не выполнена'
    }

    if (work_list.length <= 0) {
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
                        <td>Выполнена ли работа</td>
                        <td>Студент</td>
                    </tr>
                    {work_list.map(work =>
                        <tr className='d-md-table-row'>
                            <td>{work.academic_work_id}</td>
                            <td>{work.name}</td>
                            <td>{work.discipline_id}</td>
                            <td>{complitedWork(work.is_complited)}</td>
                            <td>{work.student_id.num_z}</td>
                        </tr>)}
                </table>
            </div>
        )
}

export default WorkList
