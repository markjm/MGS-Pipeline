# Auto Mouse Grimace scale

To find more info about the project and results, see here: https://journals.sagepub.com/doi/full/10.1177/1744806918763658

## The code

This repository is a mishmash of models, data, and scripts used during this project, including some unused investigations into video processing and the like. The actual code for doing the inference can be found at `label.py`, but there may be a lot of computer setup required and version matching. For that reason, I recommend following the below **Using** section if just trying to run images through the inference engine.

> Note: Check `retraining/images/pain/test.jpg` to see generally what the training images *looked like*. If your images look particularly different (especially related to lighting, background, etc), then inference may become more innacurate.

## Using

In order to support simple usage, I have created a docker container for inference.

1. Install, setup and make sure docker is running. The Docker docs have good information on setup https://docs.docker.com/get-docker/.
2. Run `docker pull markjm/mgs:latest` to pull the latest inference image
3. Put all your images into a single directory (the directory and be a nested structure of directories and images) `<some-dir>`.
4. From a **Powershell** window opened in the directory containing your images (`cd <some-dir>`), run: `docker run -it --rm -v ${PWD}:/images markjm/mgs`
5. Note the results are printed into the powershell window. Simply copy & paste them to whatever program and format you need.

> Note: sorry for the bad export experience of just printing to console. Please let me know if it is a large blocker. If so, I will build a quick "export to CSV"
 functionality.