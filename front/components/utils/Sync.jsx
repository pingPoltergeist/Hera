import {useState} from "react";
import {sync} from "../../helpers/helperApiCalls";
import styles from '/styles/components/utils/Sync.module.scss'

const Sync = () => {

    const [syncing, setSyncing] = useState(false)

    const handleSync = () => {
        setSyncing(true)
        sync()
            .then(data => setSyncing(false))
            .catch(err => setSyncing(false))
    }

    return (
        <div onClick={handleSync} className={styles.sync_container}>
            <img src="/images/utils/sync.svg" className={syncing ? 'rotating' : undefined} alt="sync"/>
        </div>
    )
}

export default Sync