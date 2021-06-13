import { Swiper, SwiperSlide } from 'swiper/react'
import styles from '/styles/components/utils/ThumbnailSlider.module.scss'
import Image from "next/image"
import Link from "next/link"


const ThumbnailSlider = ({ medias, title, type='movie' }) => {

    return (
        <div className={styles.slider_container}>
            <p className={styles.slider_title}>{title}</p>
            <Swiper breakpoints={{
                100: {
                    slidesPerView: 2,
                },
                768: {
                    slidesPerView: 4
                },
            }} spaceBetween={10} className={styles.slider_body}>
                {medias.map((media, index) => (
                    <SwiperSlide className={styles.card} key={index}>
                        <Link href={`/${type}/${media.tmdb_id}`}>
                            {media.thumbnail ? <Image layout="fill" src={media.thumbnail}/> :
                                <h2>{media.name}</h2>}
                        </Link>
                    </SwiperSlide>
                ))}
            </Swiper>
        </div>
    )
}

export default ThumbnailSlider