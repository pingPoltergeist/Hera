import MediaSlider from "../components/utils/MediaSlider"
import {getCookieToken} from "../helpers/authApiCalls"
import {getFavourites} from "../helpers/helperApiCalls"
import styles from '/styles/pages/Favourites.module.scss'

export async function getServerSideProps({ query, req, res }) {
    const token = getCookieToken(req, res)

    return getFavourites(token).then(content => {
        if (!content || content.error) {
            return {
                notFound: true,
            }
        }
        return {props: {content}}
    })
}

const favourites = ({ content }) => {

    return (
        <div className={styles.favourites_container}>
            {content && content.movies && content.movies[0] &&
            <MediaSlider type="movie" medias={content.movies} title="Movies in your favourites"/>}
            {content && content.tvs && content.tvs[0] &&
            <MediaSlider type="tv" medias={content.tvs} title="TV shows in your favourites"/>}

            {!content.movies[0] && !content.tvs[0] &&
            <div className={styles.fallback_container}>
                <h1>There are no content in your wishlist</h1>
            </div>
            }

        </div>
    )
}

export default favourites