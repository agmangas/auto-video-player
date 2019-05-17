#!/usr/bin/env python2

from subprocess import Popen, PIPE
import re
import uuid
import os
import glob
import datetime

VIDEO_DEST = "/home/pi/Videos"
VIDEO_EXT = "mp4"


def run_cmd(cmd_args):
    print("Running: {}".format(cmd_args))

    process = Popen(cmd_args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    if stdout:
        print("Stdout: {}".format(stdout))

    if stderr:
        print("Stderr: {}".format(stderr))

    if process.returncode != 0:
        raise Exception("'{}' returned error code: {}".format(
            ' '.join(cmd_args), process.returncode))

    return stdout, stderr


def mount_usb(usb_path):
    mount_path = os.path.join("/media/videousb")
    run_cmd(["mkdir", "-p", mount_path])
    run_cmd(["chmod", "770", mount_path])
    run_cmd(["mount", usb_path, mount_path])

    return mount_path


def find_usb_device():
    stdout, _ = run_cmd(["blkid"])
    print("$ blkid\n{}".format(stdout))
    results = re.findall(r"(/dev/sda[0-9]).+TYPE=\"vfat\"", stdout)

    return results[0] if len(results) else None


def find_video_file(mount_path):
    video_files = glob.glob("{}/*.{}".format(mount_path, VIDEO_EXT))
    print("USB video files: {}".format(video_files))

    return video_files[0] if len(video_files) else None


def copy_video(video_file):
    orig_name = os.path.basename(video_file).split(".")[0]
    dest_name = re.sub(r'\W+', '', orig_name) + ".{}".format(VIDEO_EXT)
    dest_path = os.path.join(VIDEO_DEST, dest_name)

    print("Copying {} to {}".format(video_file, dest_path))

    run_cmd(["cp", "-rf", video_file, dest_path])
    run_cmd(["chmod", "777", dest_path])

    return dest_path


def clean_videos_dir(file_to_keep):
    remove_files = glob.glob("{}/*.{}".format(VIDEO_DEST, VIDEO_EXT))
    remove_files = [item for item in remove_files if item != file_to_keep]

    print("Removing old videos: {}".format(remove_files))

    for file_path in remove_files:
        run_cmd(["rm", "-f", file_path])


def main():
    print("### Now: {}".format(datetime.datetime.now()))

    usb_path = find_usb_device()

    if not usb_path:
        print("No USB found")
        return

    print("USB found: {}".format(usb_path))
    print("Mounting USB")

    mount_path = mount_usb(usb_path)

    print("USB mounted to: {}".format(mount_path))

    video_file = find_video_file(mount_path)

    if not video_file:
        print("No video found")
        return

    dest_path = copy_video(video_file)
    clean_videos_dir(dest_path)


if __name__ == "__main__":
    main()
