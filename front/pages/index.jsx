import Head from 'next/head'
import styles from '../styles/pages/Home.module.scss'
import {getMovieList, getRandomMedia} from "../helpers/movieApiCalls"
import {useEffect, useState} from "react"
import MediaSlider from "../components/utils/MediaSlider"
import ThumbnailSlider from "../components/utils/ThumbnailSlider"
import {getTvList} from "../helpers/tvApiCalls"
import ActionBlock from "../components/utils/ActionBlock"
import {shorten, withAuth} from "../helpers/utilities"
import {getAllGenres, getGenre} from "../helpers/genreApiCalls"
import {ErrorBoundary} from "react-error-boundary"
import Fallback from "../components/Fallback"
import {isAuthenticated} from "../helpers/authApiCalls";


const Home = () => {

    const [hero, setHero] = useState(null)
    const [movieList, setMovieList] = useState([])
    const [tvList, setTvList] = useState([])
    const [genre, setGenre] = useState([])

    const token = isAuthenticated()

    const preload = () => {
        getRandomMedia(token).then(data => {
            if (!data) {
                return
            }
            setHero(data[0])
        })
        getMovieList('top-rated', 6).then(data => {
            setMovieList(data)
        })
        getTvList('popular', 6).then(data => {
            setTvList(data)
        })

        getAllGenres().then(data => {
            if (data) {
                let tempGenre = []
                for (const item of data) {
                    getGenre(item.tmdb_id).then(result => {
                        result.movies = result.movies.concat(result.tv_shows)
                        tempGenre.push(result)
                    })
                }
                setGenre(tempGenre)
            }
        })
    }

    useEffect(()=> {
        preload()
    }, [])

    return (
        <div className={styles.container}>
            <Head>
                <title>HERA | HOME</title>
                <meta name="description" content="Generated by create next app" />
            </Head>

            <div id="hero" className="hero hero_full" style={hero && hero.background_image ? {backgroundImage: `url(${hero.background_image})`} : {backgroundImage: `url(https://images.unsplash.com/photo-1550684376-efcbd6e3f031?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80)`}}>
                <section/>
                {hero && <div className={styles.hero_content}>
                    <img className={styles.hero_logo} src={hero.logo} alt=""/>
                    {!hero.logo && <h2 className={styles.hero_title}>{hero.name && hero.name.toUpperCase()}</h2>}
                    <p className={styles.hero_subtitle}>
                        {hero.genres && hero.genres[0] && hero.genres.map((genre, index) => (
                            <span key={index} className={styles.subtitle_span}>{genre.name}</span>
                        ))}
                    </p>
                    <p className={styles.hero_description}>{shorten(hero.description)}</p>

                    <ActionBlock media={hero}/>
                </div>}
            </div>

            <ErrorBoundary FallbackComponent={Fallback}>
                {movieList && movieList[0] ? <ThumbnailSlider medias={movieList} title="Popular Worldwide" /> : null}
            </ErrorBoundary>

            <ErrorBoundary FallbackComponent={Fallback}>
                {movieList && movieList[0] ? <MediaSlider medias={movieList} title="Recommended movies for you" type="movie" /> : null}
            </ErrorBoundary>

            <ErrorBoundary FallbackComponent={Fallback}>
                {tvList && tvList[0] ? <MediaSlider medias={tvList} title="Popular shows worldwide" type="tv" size="thin" /> : null}
            </ErrorBoundary>

            <ErrorBoundary FallbackComponent={Fallback}>
                {genre && genre[0] ? genre.map(singleGenre => (singleGenre.movies.length >= 4 &&
                    <ThumbnailSlider medias={singleGenre.movies} title={`Popular in ${singleGenre.name}`} />
                )) : null}
            </ErrorBoundary>

        </div>
    )
}


export default withAuth(Home)