#
# DeepLabCut Toolbox (deeplabcut.org)
# © A. & M.W. Mathis Labs
# https://github.com/DeepLabCut/DeepLabCut
#
# Please see AUTHORS for contributors.
# https://github.com/DeepLabCut/DeepLabCut/blob/master/AUTHORS
#
# Licensed under GNU Lesser General Public License v3.0
#


import os
import shutil
import warnings
from pathlib import Path
from deeplabcut import DEBUG
from deeplabcut.utils.auxfun_videos import VideoReader


def create_new_project_horse(
    horse_name,
    horse_father,
    horse_mother,
    horse_owner,
    horse_seller,
    horse_buyer,
    horse_type,
    video,
    working_directory=None,
    copy_video=False,
    videotype="",
):
    r"""Create the necessary folders and files for a new horse project.

    Creating a new project involves creating the project directory, sub-directories and
    a basic configuration file. The configuration file is loaded with the default
    values. Change its parameters to your projects need.

    Parameters
    ----------
    horse_name : string
        The name of the horse.
    
    horse_father : string
        The name of the father.
        
    horse_owner : string
        The name of the owner.
    
    horse_seller : string
        The name of the seller.
        
    horse_buyer : string
        The name of the buyer.
        
    horse_type : string
        The type of the horse.

    video : str
        A string representing the full path of the video to include in the
        project.

    working_directory : string, optional
        The directory where the project will be created. The default is the
        ``current working directory``.

    copy_video : bool, optional, Default: False.
        If True, the video are copied to the ``video`` directory. If False, symlinks
        of the video will be created in the ``project/video`` directory; in the event
        of a failure to create symbolic link, video will be moved instead.

    Returns
    -------
    str
        Path to the new project configuration file.
    """
    from datetime import datetime as dt
    from deeplabcut.utils import auxiliaryfunctions_horse

    months_3letter = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }

    date = dt.today()
    month = months_3letter[date.month]
    day = date.day
    d = str(month[0:3] + str(day))
    date = dt.today().strftime("%Y-%m-%d")
    if working_directory is None:
        working_directory = "."
    wd = Path(working_directory).resolve()
    project_name = "{pn}-{exp}-{date}".format(pn=horse_name, exp=horse_owner, date=date)
    project_path = wd / project_name

    # Create project and sub-directories
    if not DEBUG and project_path.exists():
        print('Project "{}" already exists!'.format(project_path))
        return os.path.join(str(project_path), "config.yaml")
    video_path = project_path / "video"

    for p in [video_path]:
        p.mkdir(parents=True, exist_ok=DEBUG)
        print('Created "{}"'.format(p))

    # Add video in the folder. 
    videos = []
    # Check if it is a file
    if os.path.isfile(video):
        videos = [video]

    videos = [Path(vp) for vp in videos]
    destinations = [video_path.joinpath(vp.name) for vp in videos]
    if copy_video:
        print("Copying the video")
        for src, dst in zip(videos, destinations):
            shutil.copy(
                os.fspath(src), os.fspath(dst)
            )  # https://www.python.org/dev/peps/pep-0519/
    else:
        # creates the symlinks of the video and puts it in the video directory.
        print("Attempting to create a symbolic link of the video ...")
        for src, dst in zip(videos, destinations):
            if dst.exists() and not DEBUG:
                raise FileExistsError("Video {} exists already!".format(dst))
            try:
                src = str(src)
                dst = str(dst)
                os.symlink(src, dst)
                print("Created the symlink of {} to {}".format(src, dst))
            except OSError:
                try:
                    import subprocess

                    subprocess.check_call("mklink %s %s" % (dst, src), shell=True)
                except (OSError, subprocess.CalledProcessError):
                    print(
                        "Symlink creation impossible (exFat architecture?): "
                        "copying the video instead."
                    )
                    shutil.copy(os.fspath(src), os.fspath(dst))
                    print("{} copied to {}".format(src, dst))
            videos = destinations

    if copy_video:
        videos = destinations  # in this case the *new* location should be added to the config file

    # adds the video list to the config.yaml file
    for video in videos:
        print(video)
        try:
            # For windows os.path.realpath does not work and does not link to the real video. [old: rel_video_path = os.path.realpath(video)]
            rel_video_path = str(Path.resolve(Path(video)))
        except:
            rel_video_path = os.readlink(str(video))

        try:
            vid = VideoReader(rel_video_path)
        except IOError:
            warnings.warn("Cannot open the video file! Skipping to the next one...")
            os.remove(video)  # Removing the video or link from the project

    if not rel_video_path:
        # Silently sweep the files that were already written.
        shutil.rmtree(project_path, ignore_errors=True)
        warnings.warn(
            "No valid videos were found. The project was not created... "
            "Verify the video files and re-create the project."
        )
        return "nothingcreated"

    # Set values to config file:
    cfg_file, ruamelFile = auxiliaryfunctions_horse.create_config_template_horse()
    # common parameters:
    cfg_file["horse_name"] = horse_name
    cfg_file["horse_father"] = horse_father
    cfg_file["horse_mother"] = horse_mother
    cfg_file["horse_owner"] = horse_owner
    cfg_file["horse_seller"] = horse_seller
    cfg_file["horse_buyer"] = horse_buyer
    cfg_file["horse_type"] = horse_type
    cfg_file["video_type"] = videotype
    cfg_file["video_path"] = rel_video_path
    cfg_file["project_path"] = str(project_path)
    cfg_file["date"] = d

    projconfigfile = os.path.join(str(project_path), "config.yaml")
    # Write dictionary to yaml  config file
    auxiliaryfunctions_horse.write_config_horse(projconfigfile, cfg_file)

    print('Generated "{}"'.format(project_path / "config.yaml"))
    print(
        "\nA new project with name %s is created at %s and a configurable file (config.yaml) is stored there. Change the parameters in this file to adapt to your project's needs.\n Once you have changed the configuration file, use the function 'extract_frames' to select frames for labeling.\n. [OPTIONAL] Use the function 'add_new_videos' to add new videos to your project (at any stage)."
        % (project_name, str(wd))
    )
    return projconfigfile
