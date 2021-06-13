import styles from '/styles/components/admin/Overview.module.scss'
import {useEffect, useState} from "react"
import {getCount} from "../../helpers/settingsApiCalls"

const Overview = ({token}) => {

    const [movieCount, setMovieCount] = useState(0)
    const [tvCount, setTvCount] = useState(0)
    const [userCount, setUserCount] = useState(0)

    const preload = () => {
        getCount(token, 'movie').then(response => setMovieCount(response.count))
        getCount(token, 'tv').then(response => setTvCount(response.count))
        getCount(token, 'user').then(response => setUserCount(response.count))
    }

    useEffect(() => {
        preload()
    }, [])

    return (
        <div className={styles.overview_container}>
            <div className={styles.single_overview_container}>
                <p className={styles.overview_subtitle}>Available total</p>
                <h5 className={styles.overview_title}>{movieCount}</h5>
                <p className={styles.overview_subtitle}>movies</p>
            </div>
            <div className={styles.single_overview_container}>
                <p className={styles.overview_subtitle}>Available total</p>
                <h5 className={styles.overview_title}>{tvCount}</h5>
                <p className={styles.overview_subtitle}>TV shows</p>
            </div>
            <div className={styles.single_overview_container}>
                <p className={styles.overview_subtitle}>Available total</p>
                <h5 className={styles.overview_title}>{userCount}</h5>
                <p className={styles.overview_subtitle}>active users</p>
            </div>
        </div>
    )
}

export default Overview