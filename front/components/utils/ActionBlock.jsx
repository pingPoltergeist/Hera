import styles from "/styles/components/utils/ActionBlock.module.scss"
import ReactPlayer from 'react-player'
import Link from "next/link"
import MoreAction from "./MoreAction"
import {useState} from "react"
import { AnimatePresence } from "framer-motion";


const ActionBlock = ({type="movie", media, videoID, absolute = false}) => {

    const [moreActionFlag, setMoreActionFlag] = useState(false)

    return (!media ? null :
        <div className={absolute ? styles.absolute : ''}>
            {absolute && media && media.trailer && <p className={styles.trailer_heading}>WATCH TRAILER:</p>}
            {absolute && media && media.trailer && <div className={styles.video_block}>
                <ReactPlayer playing light controls url={media && media.trailer && `${media.trailer}`} className={styles.video} width="100%" height="100%"/>
            </div> }
            <div className={styles.action_block}>

                <AnimatePresence>
                    {moreActionFlag && <MoreAction media={media} type={type} flag={moreActionFlag} setFlag={setMoreActionFlag}/>}
                </AnimatePresence>

                <div className="more_action_button" onClick={() => setMoreActionFlag(!moreActionFlag)}>
                    <img className={styles.hero_logo} src="/images/utils/three-dots.svg" alt=""/>
                </div>

                {type === "tv"
                    ?
                    media && media.seasons && <Link href={`/watch/${videoID || Object.values(media.seasons)[0][0].tmdb_id}`}>
                        <a className="button">START WATCHING</a>
                    </Link>

                    :
                    media && <Link href={`/watch/${media.tmdb_id}`}>
                        <a className="button">
                            {type === "movie" ? "WATCH IT NOW" : "START WATCHING"}
                        </a>
                    </Link>
                }

            </div>
        </div>
    )
}

export default ActionBlock