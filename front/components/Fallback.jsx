import styles from '/styles/components/Fallback.module.scss'

const Fallback = () => {
    return (
        <div className={styles.fallback_container}>
            <h3 className={styles.fallback_heading}>Whoops! We are having issues :(</h3>
            <p className={styles.fallback_description}>It looks like that this section can not be loaded right now. If the problem persists, contact us.</p>
        </div>
    )
}

export default Fallback