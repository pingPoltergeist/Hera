import styles from "/styles/components/utils/Slider.module.scss"
import Image from "next/image"
import Link from "next/link"

const MediaSlider = ({medias, title, type='collection', size='normal', preload=false}) => {
    return (
        <div className={styles.slider_container}>
            {title && <p className={styles.slider_title}>{title}</p>}
            <div className={styles.slider_body}>
                {medias && medias.map((media, index) => (
                    <Link key={index} href={`/${type}/${media.tmdb_id}`}>
                        <div className={`${styles.slider_card} ${size==='thin' ? styles.thin : styles.normal}`}>
                            <Image loading={"eager"} quality={5} src={media.poster_image || '/hello.jpeg'} priority={preload} layout='fill' objectFit={"cover"}/>
                        </div>
                    </Link>
                ))}
            </div>
        </div>
    )
}

export default MediaSlider