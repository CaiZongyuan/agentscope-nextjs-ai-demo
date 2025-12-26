
# Image Generation

The AI SDK provides the [`generateImage`](/docs/reference/ai-sdk-core/generate-image)
function to generate images based on a given prompt using an image model.

```tsx
import { generateImage } from 'ai';
import { openai } from '@ai-sdk/openai';

const { image } = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'Santa Claus driving a Cadillac',
});
```

You can access the image data using the `base64` or `uint8Array` properties:

```tsx
const base64 = image.base64; // base64 image data
const uint8Array = image.uint8Array; // Uint8Array image data
```

## Settings

### Size and Aspect Ratio

Depending on the model, you can either specify the size or the aspect ratio.

##### Size

The size is specified as a string in the format `{width}x{height}`.
Models only support a few sizes, and the supported sizes are different for each model and provider.

```tsx highlight={"7"}
import { generateImage } from 'ai';
import { openai } from '@ai-sdk/openai';

const { image } = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'Santa Claus driving a Cadillac',
  size: '1024x1024',
});
```

##### Aspect Ratio

The aspect ratio is specified as a string in the format `{width}:{height}`.
Models only support a few aspect ratios, and the supported aspect ratios are different for each model and provider.

```tsx highlight={"7"}
import { generateImage } from 'ai';
import { vertex } from '@ai-sdk/google-vertex';

const { image } = await generateImage({
  model: vertex.image('imagen-4.0-generate-001'),
  prompt: 'Santa Claus driving a Cadillac',
  aspectRatio: '16:9',
});
```

### Generating Multiple Images

`generateImage` also supports generating multiple images at once:

```tsx highlight={"7"}
import { generateImage } from 'ai';
import { openai } from '@ai-sdk/openai';

const { images } = await generateImage({
  model: openai.image('dall-e-2'),
  prompt: 'Santa Claus driving a Cadillac',
  n: 4, // number of images to generate
});
```

<Note>
  `generateImage` will automatically call the model as often as needed (in
  parallel) to generate the requested number of images.
</Note>

Each image model has an internal limit on how many images it can generate in a single API call. The AI SDK manages this automatically by batching requests appropriately when you request multiple images using the `n` parameter. By default, the SDK uses provider-documented limits (for example, DALL-E 3 can only generate 1 image per call, while DALL-E 2 supports up to 10).

If needed, you can override this behavior using the `maxImagesPerCall` setting when generating your image. This is particularly useful when working with new or custom models where the default batch size might not be optimal:

```tsx
const { images } = await generateImage({
  model: openai.image('dall-e-2'),
  prompt: 'Santa Claus driving a Cadillac',
  maxImagesPerCall: 5, // Override the default batch size
  n: 10, // Will make 2 calls of 5 images each
});
```

### Providing a Seed

You can provide a seed to the `generateImage` function to control the output of the image generation process.
If supported by the model, the same seed will always produce the same image.

```tsx highlight={"7"}
import { generateImage } from 'ai';
import { openai } from '@ai-sdk/openai';

const { image } = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'Santa Claus driving a Cadillac',
  seed: 1234567890,
});
```

### Provider-specific Settings

Image models often have provider- or even model-specific settings.
You can pass such settings to the `generateImage` function
using the `providerOptions` parameter. The options for the provider
(`openai` in the example below) become request body properties.

```tsx highlight={"9"}
import { generateImage } from 'ai';
import { openai } from '@ai-sdk/openai';

const { image } = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'Santa Claus driving a Cadillac',
  size: '1024x1024',
  providerOptions: {
    openai: { style: 'vivid', quality: 'hd' },
  },
});
```

### Abort Signals and Timeouts

`generateImage` accepts an optional `abortSignal` parameter of
type [`AbortSignal`](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal)
that you can use to abort the image generation process or set a timeout.

```ts highlight={"7"}
import { openai } from '@ai-sdk/openai';
import { generateImage } from 'ai';

const { image } = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'Santa Claus driving a Cadillac',
  abortSignal: AbortSignal.timeout(1000), // Abort after 1 second
});
```

### Custom Headers

`generateImage` accepts an optional `headers` parameter of type `Record<string, string>`
that you can use to add custom headers to the image generation request.

```ts highlight={"7"}
import { openai } from '@ai-sdk/openai';
import { generateImage } from 'ai';

const { image } = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'Santa Claus driving a Cadillac',
  headers: { 'X-Custom-Header': 'custom-value' },
});
```

### Warnings

If the model returns warnings, e.g. for unsupported parameters, they will be available in the `warnings` property of the response.

```tsx
const { image, warnings } = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'Santa Claus driving a Cadillac',
});
```

### Additional provider-specific meta data

Some providers expose additional meta data for the result overall or per image.

```tsx
const prompt = 'Santa Claus driving a Cadillac';

const { image, providerMetadata } = await generateImage({
  model: openai.image('dall-e-3'),
  prompt,
});

const revisedPrompt = providerMetadata.openai.images[0]?.revisedPrompt;

console.log({
  prompt,
  revisedPrompt,
});
```

The outer key of the returned `providerMetadata` is the provider name. The inner values are the metadata. An `images` key is always present in the metadata and is an array with the same length as the top level `images` key.

### Error Handling

When `generateImage` cannot generate a valid image, it throws a [`AI_NoImageGeneratedError`](/docs/reference/ai-sdk-errors/ai-no-image-generated-error).

This error occurs when the AI provider fails to generate an image. It can arise due to the following reasons:

- The model failed to generate a response
- The model generated a response that could not be parsed

The error preserves the following information to help you log the issue:

- `responses`: Metadata about the image model responses, including timestamp, model, and headers.
- `cause`: The cause of the error. You can use this for more detailed error handling

```ts
import { generateImage, NoImageGeneratedError } from 'ai';

try {
  await generateImage({ model, prompt });
} catch (error) {
  if (NoImageGeneratedError.isInstance(error)) {
    console.log('NoImageGeneratedError');
    console.log('Cause:', error.cause);
    console.log('Responses:', error.responses);
  }
}
```

## Generating Images with Language Models

Some language models such as Google `gemini-2.5-flash-image-preview` support multi-modal outputs including images.
With such models, you can access the generated images using the `files` property of the response.

```ts
import { google } from '@ai-sdk/google';
import { generateText } from 'ai';

const result = await generateText({
  model: google('gemini-2.5-flash-image-preview'),
  prompt: 'Generate an image of a comic cat',
});

for (const file of result.files) {
  if (file.mediaType.startsWith('image/')) {
    // The file object provides multiple data formats:
    // Access images as base64 string, Uint8Array binary data, or check type
    // - file.base64: string (data URL format)
    // - file.uint8Array: Uint8Array (binary data)
    // - file.mediaType: string (e.g. "image/png")
  }
}
```
