import {useEffect, useState} from "react";
import {getAllMovies, getRandomMedia} from "../../helpers/movieApiCalls";
import styles from "/styles/pages/movie/Home.module.scss"
import MediaSlider from "../../components/utils/MediaSlider";
import ActionBlock from "../../components/utils/ActionBlock";
import {shorten, withAuth} from "../../helpers/utilities";
import Fallback from "../../components/Fallback";
import {ErrorBoundary} from "react-error-boundary";
import {isAuthenticated} from "../../helpers/authApiCalls";


const movie = () => {

    const [hero, setHero] = useState([])
    const [movies, setMovies] = useState([])
    const token = isAuthenticated()

    const preload = () => {
        getRandomMedia(token, 'movie', 2).then(data => {
            setHero(data)
        })
        getAllMovies().then(data => {
            setMovies(data)
        })
    }
    useEffect(() => {
        preload()
    }, [])
    return (
        <div className={styles.container}>
            <div className={styles.hero} style={hero && hero[0] ? {} : {backgroundImage: `url(https://images.unsplash.com/photo-1550684376-efcbd6e3f031?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80)`}}>
                {hero && hero[0] && hero.map((movie, index) => (
                    <div key={index} className={styles.hero_side} >
                        <div className={styles.background_container} style={movie && {backgroundImage: `url(${movie.background_image})`}}></div>
                        <section/>
                        <img src={movie && movie.logo} alt=""/>
                        {!movie.logo && <h2 className={styles.hero_title}>{movie.name && movie.name.toUpperCase()}</h2>}
                        <p className={styles.hero_description}>{movie && shorten(movie.description)}</p>

                        <ActionBlock type="movie" media={movie} />
                    </div>
                ))}
            </div>

            <ErrorBoundary FallbackComponent={Fallback}>
                <MediaSlider medias={movies} type={'movie'}/>
            </ErrorBoundary>

        </div>
    )
}

export default withAuth(movie)