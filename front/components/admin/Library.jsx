import styles from '/styles/components/admin/Library.module.scss'
import {useState} from "react";
import {handleMediaFolder} from "../../helpers/settingsApiCalls";
import {useRouter} from "next/router";
import '/helpers/utilities'

const Library = ({folders, type="movie", token}) => {

    const router = useRouter()

    const [newLibrary, setNewLibrary] = useState('')

    const handleChange = (event) => {
        setNewLibrary(event.target.value)
    }

    const handleSubmit = () => {
        handleMediaFolder(token, newLibrary, type, 'PUT').then(response => {console.log(response)})
    }

    const handleDelete = (folder) => {
        handleMediaFolder(token, folder, type, 'DELETE').then(response => {return null})
        router.reload()
    }

    return (
        <div className={styles.library_box}>
            <h3 className={styles.library_title}>{type.toTitleCase()} Library</h3>
            {folders.map((folder, index) => (
                <div key={index} className={styles.single_folder_box}>
                    <p className={styles.single_folder_name}>{folder}</p>
                    <img onClick={() => handleDelete(folder)} src="/images/utils/delete.svg" alt="delete"/>
                </div>
            ))}

            <form>
                <input required onChange={handleChange} type="text" placeholder={`Add new ${type} library`} className={styles.single_folder_box}/>
                <button onClick={handleSubmit} className={styles.library_button} type="submit">Add {type} library</button>
            </form>
        </div>
    )
}

export default Library