# Python
import time

# Django
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

# AstroBin
from astrobin.models import (
    Image,
    Telescope,
    Mount,
    Camera,
    FocalReducer,
    Software,
    Filter,
    Accessory,
    DeepSky_Acquisition)


class ImageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'test', 'test@test.com', 'password')

    def tearDown(self):
        self.user.delete()


    ###########################################################################
    # HELPERS                                                                 #
    ###########################################################################

    def _do_upload(self, filename):
        return self.client.post(
            reverse('image_upload_process'),
            {'image_file': open(filename, 'rb')},
            follow = True)

    def _do_upload_revision(self, image, filename):
        return self.client.post(
            reverse('image_revision_upload_process'),
            {'image_id': image.id, 'image_file': open(filename, 'rb')},
            follow = True)

    def _get_last_image(self):
        return Image.objects.all().order_by('-id')[0]


    def _assert_message(self, response, tags, content):
        storage = response.context[0]['messages']
        for message in storage:
            self.assertEqual(message.tags, tags)
            self.assertTrue(content in message.message)


    ###########################################################################
    # View tests                                                              #
    ###########################################################################

    def test_image_upload_process_view(self):
        self.client.login(username = 'test', password = 'password')

        # Test file with invalid extension
        response = self._do_upload('astrobin/fixtures/invalid_file')
        self.assertRedirects(
            response,
            reverse('image_upload'),
            status_code = 302,
            target_status_code = 200)
        self._assert_message(response, "error unread", "Invalid image")

        # Test file with invalid content
        response = self._do_upload('astrobin/fixtures/invalid_file.jpg')
        self.assertRedirects(
            response,
            reverse('image_upload'),
            status_code = 302,
            target_status_code = 200)
        self._assert_message(response, "error unread", "Invalid image")

        # Test successful upload
        response = self._do_upload('astrobin/fixtures/test.jpg')
        self.assertRedirects(
            response,
            reverse('image_edit_watermark', kwargs = {'id': 1}),
            status_code = 302,
            target_status_code = 200)

        image = Image.objects.get(pk = 1)
        self.assertEqual(image.title, u"")

        # Test watermark
        response = self.client.post(
            reverse('image_edit_save_watermark'),
            {
                'image_id': 1,
                'watermark': True,
                'watermark_text': "Watermark test",
                'watermark_position': 0,
                'watermark_opacity': 100
            },
            follow = True)
        image = Image.objects.get(pk = 1)
        self.assertRedirects(
            response,
            reverse('image_edit_basic', kwargs = {'id': 1}),
            status_code = 302,
            target_status_code = 200)
        self.assertEqual(image.watermark, True)
        self.assertEqual(image.watermark_text, "Watermark test")
        self.assertEqual(image.watermark_position, 0)
        self.assertEqual(image.watermark_opacity, 100)

        # Test basic settings
        response = self.client.post(
            reverse('image_edit_save_basic'),
            {
                'image_id': 1,
                'submit_gear': True,
                'title': "Test title",
                'link': "http://www.example.com",
                'link_to_fits': "http://www.example.com/fits",
                'subject_type': 600,
                'solar_system_main_subject': 0,
                'locations': [],
                'description': "Image description",
                'allow_comments': True
            },
            follow = True)
        image = Image.objects.get(pk = 1)
        self.assertRedirects(
            response,
            reverse('image_edit_gear', kwargs = {'id': 1}),
            status_code = 302,
            target_status_code = 200)
        self.assertEqual(image.title, "Test title")
        self.assertEqual(image.link, "http://www.example.com")
        self.assertEqual(image.link_to_fits, "http://www.example.com/fits")
        self.assertEqual(image.subject_type, 600)
        self.assertEqual(image.solar_system_main_subject, 0)
        self.assertEqual(image.locations.count(), 0)
        self.assertEqual(image.description, "Image description")
        self.assertEqual(image.allow_comments, True)

        # Test gear
        imaging_telescopes = [
            Telescope.objects.create(
                make = "Test make", name = "Test imaging telescope")]
        guiding_telescopes = [
            Telescope.objects.create(
                make = "Test make", name = "Test guiding telescope")]
        mounts = [
            Mount.objects.create(
                make = "Test make", name = "Test mount")]
        imaging_cameras = [
            Camera.objects.create(
                make = "Test make", name = "Test imaging camera")]
        guiding_cameras = [
            Camera.objects.create(
                make = "Test make", name = "Test guiding camera")]
        focal_reducers = [
            FocalReducer.objects.create(
                make = "Test make", name = "Test focal reducer")]
        software = [
            Software.objects.create(
                make = "Test make", name = "Test software")]
        filters = [
            Filter.objects.create(
                make = "Test make", name = "Test filter")]
        accessories = [
            Accessory.objects.create(
                make = "Test make", name = "Test accessory")]

        profile = self.user.userprofile
        profile.telescopes = imaging_telescopes + guiding_telescopes
        profile.mounts = mounts
        profile.cameras = imaging_cameras + guiding_cameras
        profile.focal_reducers = focal_reducers
        profile.software = software
        profile.filters = filters
        profile.accessories = accessories

        response = self.client.post(
            reverse('image_edit_save_gear'),
            {
                'image_id': 1,
                'submit_acquisition': True,
                'imaging_telescopes': ','.join(["%d" % x.pk for x in imaging_telescopes]),
                'guiding_telescopes': ','.join(["%d" % x.pk for x in guiding_telescopes]),
                'mounts': ','.join(["%d" % x.pk for x in mounts]),
                'imaging_cameras': ','.join(["%d" % x.pk for x in imaging_cameras]),
                'guiding_cameras': ','.join(["%d" % x.pk for x in guiding_cameras]),
                'focal_reducers': ','.join(["%d" % x.pk for x in focal_reducers]),
                'software': ','.join(["%d" % x.pk for x in software]),
                'filters': ','.join(["%d" % x.pk for x in filters]),
                'accessories': ','.join(["%d" % x.pk for x in accessories])
            },
            follow = True)
        image = Image.objects.get(pk = 1)
        self.assertRedirects(
            response,
            reverse('image_edit_acquisition', kwargs = {'id': 1}),
            status_code = 302,
            target_status_code = 200)

        # Test simple deep sky acquisition
        today = time.strftime('%Y-%m-%d')
        response = self.client.post(
            reverse('image_edit_save_acquisition'),
            {
                'image_id': 1,
                'edit_type': 'deep_sky',
                'advanced': 'false',
                'date': today,
                'number': 10,
                'duration': 1200
            },
            follow = True)
        self.assertRedirects(
            response,
            reverse('image_detail', kwargs = {'id': 1}),
            status_code = 302,
            target_status_code = 200)

        image = Image.objects.get(pk = 1)
        acquisition = image.acquisition_set.all()[0].deepsky_acquisition
        self.assertEqual(acquisition.date.strftime('%Y-%m-%d'), today)
        self.assertEqual(acquisition.number, 10)
        self.assertEqual(acquisition.duration, 1200)

        image.delete()

    def test_image_detail_view(self):
        self.client.login(username = 'test', password = 'password')
        self._do_upload('astrobin/fixtures/test.jpg')
        image = self._get_last_image()
        response = self.client.get(reverse('image_detail', kwargs = {'id': image.id}))
        self.assertEqual(response.status_code, 200)

    def test_image_flag_thumbs_view(self):
        self.client.login(username = 'test', password = 'password')
        self._do_upload('astrobin/fixtures/test.jpg')
        image = self._get_last_image()
        response = self.client.post(
            reverse('image_flag_thumbs', kwargs = {'id': image.id}))
        self.assertRedirects(
            response,
            reverse('image_detail', kwargs = {'id': image.id}),
            status_code = 302,
            target_status_code = 200)

    def test_image_thumb_view(self):
        self.client.login(username = 'test', password = 'password')
        self._do_upload('astrobin/fixtures/test.jpg')
        image = self._get_last_image()
        response = self.client.get(
            reverse('image_thumb', kwargs = {
                'id': image.id,
                'alias': 'regular'
            }))
        self.assertEqual(response.status_code, 200)

    def test_image_rawthumb_view(self):
        self.client.login(username = 'test', password = 'password')
        self._do_upload('astrobin/fixtures/test.jpg')
        image = self._get_last_image()
        response = self.client.get(
            reverse('image_rawthumb', kwargs = {
                'id': image.id,
                'alias': 'regular'
            }),
            follow = True)
        self.assertRedirects(
            response,
            image.thumbnail('regular'),
            status_code = 302,
            target_status_code = 200)

    def test_image_full_view(self):
        self.client.login(username = 'test', password = 'password')
        self._do_upload('astrobin/fixtures/test.jpg')
        image = self._get_last_image()
        response = self.client.get(reverse('image_full', kwargs = {'id': image.id}))
        self.assertEqual(response.status_code, 200)

    def test_image_upload_revision_process_view(self):
        self.client.login(username = 'test', password = 'password')
        self._do_upload('astrobin/fixtures/test.jpg')
        image = self._get_last_image()

        # Test file with invalid extension
        response = self._do_upload_revision(image, 'astrobin/fixtures/invalid_file')
        self.assertRedirects(
            response,
            reverse('image_detail', kwargs = {'id': image.id}),
            status_code = 302,
            target_status_code = 200)
        self._assert_message(response, "error unread", "Invalid image")

        # Test file with invalid content
        response = self._do_upload_revision(image, 'astrobin/fixtures/invalid_file.jpg')
        self.assertRedirects(
            response,
            reverse('image_detail', kwargs = {'id': image.id}),
            status_code = 302,
            target_status_code = 200)
        self._assert_message(response, "error unread", "Invalid image")

        # Test successful upload
        response = self._do_upload_revision(image, 'astrobin/fixtures/test.jpg')
        self.assertRedirects(
            response,
            reverse('image_detail', kwargs = {'id': image.id, 'r': 'B'}),
            status_code = 302,
            target_status_code = 200)
        self._assert_message(response, "success unread", "Image uploaded")
        image = self._get_last_image()
        self.assertEqual(image.revisions.count(), 1)

    def test_image_edit_make_final_view(self):
        self.client.login(username = 'test', password = 'password')

        self._do_upload('astrobin/fixtures/test.jpg')
        image = self._get_last_image()

        self._do_upload_revision(image, 'astrobin/fixtures/test.jpg')
        image = self._get_last_image()

        response = self.client.get(
            reverse('image_edit_make_final', kwargs = {'id': image.id}),
            follow = True)
        self.assertRedirects(
            response,
            reverse('image_detail', kwargs = {'id': 1}),
            status_code = 302,
            target_status_code = 200)
        image = self._get_last_image()
        self.assertEqual(image.is_final, True)
        self.assertEqual(image.revisions.all()[0].is_final, False)

    def test_image_edit_revision_make_final_view(self):
        self.client.login(username = 'test', password = 'password')

        self._do_upload('astrobin/fixtures/test.jpg')
        image = self._get_last_image()

        # Upload revision B
        self._do_upload_revision(image, 'astrobin/fixtures/test.jpg')

        # Upload revision C
        self._do_upload_revision(image, 'astrobin/fixtures/test.jpg')

        # Check that C is final
        image = self._get_last_image()
        c = image.revisions.order_by('-label')[0]
        b = image.revisions.order_by('-label')[1]
        self.assertEqual(image.is_final, False)
        self.assertEqual(c.is_final, True)
        self.assertEqual(b.is_final, False)

        # Make B final
        response = self.client.get(
            reverse('image_edit_revision_make_final', kwargs = {'id': b.id}),
            follow = True)
        self.assertRedirects(
            response,
            reverse('image_detail', kwargs = {'id': 1, 'r': b.label}),
            status_code = 302,
            target_status_code = 200)

        # Check that B is now final
        image = self._get_last_image()
        c = image.revisions.order_by('-label')[0]
        b = image.revisions.order_by('-label')[1]
        self.assertEqual(image.is_final, False)
        self.assertEqual(c.is_final, False)
        self.assertEqual(b.is_final, True)
