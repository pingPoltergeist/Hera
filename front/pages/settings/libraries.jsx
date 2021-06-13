import AdminNav from "../../components/admin/AdminNav"
import Library from "../../components/admin/Library"
import {useEffect, useState} from "react"
import {isAuthenticated} from "../../helpers/authApiCalls"
import {getMediaFolders} from "../../helpers/settingsApiCalls";
import Fallback from "../../components/Fallback";
import {ErrorBoundary} from "react-error-boundary";

const libraries = () => {

    const token = isAuthenticated()

    const [movieLibrary, setMovieLibrary] = useState([])
    const [tvLibrary, setTvLibrary] = useState([])

    const preload = () => {
        getMediaFolders(token).then(response => {
            setMovieLibrary(response.movie_dir)
            setTvLibrary(response.tv_dir)
        })
    }

    useEffect(() => {
        preload()
    }, [])

    return (
        <div className="admin_page">
            <AdminNav active="overview"/>

            <h1 className="admin_page_title">Hera Dashboard — Libraries</h1>
            <p className="admin_page_description">This is the libraries page of your Hera installation. There are two types of libraries, movie library and TV show library. You can add new library and delete existing libraries from this page. For more information about how to add a new library please refer to the Hera documentation.</p>

            <ErrorBoundary FallbackComponent={Fallback}>
                <Library folders={movieLibrary} type="movie" token={token}/>
                <Library folders={tvLibrary} type="tv" token={token}/>
            </ErrorBoundary>
        </div>
    )
}

export default libraries