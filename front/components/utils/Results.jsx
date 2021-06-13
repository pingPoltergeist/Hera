import styles from '/styles/components/utils/Results.module.scss'
import Image from "next/image";
import Link from "next/link"

const Results = ({results}) => {
    return (
        <div className={styles.results_container}>
            {results && results[0] && results.map((result, index) => (
                <Link key={index} href={`/movie/${result.tmdb_id}`}>
                    <div key={index} className={styles.single_result}>
                        {result.poster_image && <Image src={result.poster_image} priority layout='fill' objectFit={"cover"}/>}
                    </div>
                </Link>
            ))}

            {!results || !results[0] && <h2>No Result Found</h2>}
        </div>
    )
}

export default Results