import click
import numpy as np
import orjson


def get_payload(shape, input_name="conv2d_input", datatype="FP32"):
    data = np.random.rand(*shape)
    return {
        "inputs": [
            {
                "name": input_name,
                "data": data.flatten().tolist(),
                "datatype": datatype,
                "shape": data.shape,
            }
        ],
        "outputs": [{"name": "dense_1", "parameters": {"binary_data": False}}],
    }


@click.command()
@click.option("--batch-size", "-b", default=10, type=int)
@click.option("--instances", "-i", default=500, type=int)
@click.option("--file-name", "-f", default="batch-input.txt", type=str)
def cli(batch_size, instances, file_name):
    np.random.seed(0)

    shape = (batch_size, 28, 28, 1)
    with open(file_name, "wb") as f:
        for n in range(instances):
            x = get_payload(shape)
            f.write(orjson.dumps(x))
            f.write(b"\n")


if __name__ == "__main__":
    cli()
