import styles from '/styles/components/utils/Search.module.scss'
import {useState} from "react";
import {search} from "../../helpers/helperApiCalls";
import Results from "./Results";
import {Router} from "next/router";

const Search = () => {

    const [query, setQuery] = useState('')
    const [result, setResult] = useState([])

    Router.events.on('routeChangeStart', () => {
        setQuery('')
    })

    const handleChange = (event) => {
        setQuery(event.target.value)
        search(event.target.value).then(data => setResult(data))

        if (!event.target.value) {
            setQuery('')
        }
    }

    return (
        <div className={styles.search_container}>
            <img src="/images/utils/search.svg" alt="search"/>
            <input onChange={handleChange} value={query} className={styles.search_input} type="text" placeholder="Search anything"/>
            <img onClick={() => {setQuery('')}} className={styles.close_button} style={query ? {visibility: "visible"} : {}} src="/images/utils/close.svg" alt="search"/>
            {query && <Results results={result}/>}
        </div>
    )
}

export default Search